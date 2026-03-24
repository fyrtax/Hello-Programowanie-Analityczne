import pandas as pd
import os as os
import time

import matplotlib.pyplot as plt
from ultralytics import YOLO


import numpy as np
import cv2
import glob
from tqdm import tqdm


def calculate_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)

    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    iou = interArea / float(boxAArea + boxBArea - interArea) if float(boxAArea + boxBArea - interArea) > 0 else 0
    return iou


def read_kitti_labels(label_path):
    truths = {'Car': [], 'Pedestrian': []}
    if not os.path.exists(label_path):
        return truths
    with open(label_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            obj_type = parts[0]
            if obj_type in ['Car', 'Pedestrian']:
                bbox = [float(parts[4]), float(parts[5]), float(parts[6]), float(parts[7])]
                truths[obj_type].append(bbox)
    return truths


def main():
    models_to_test = {
        'YOLO26n': 'yolo26n.pt',
        'YOLO26s': 'yolo26s.pt',
        'YOLO26m': 'yolo26m.pt',
        'YOLO26l': 'yolo26l.pt',
        'YOLO26x': 'yolo26x.pt',
        'YOLO11x': 'yolo11x.pt'
    }

    images_paths = sorted(glob.glob('images/*4.jpg'))

    output_dir = 'results'
    os.makedirs(output_dir, exist_ok=True)

    results = {}
    fps_results = {}

    for model_name, model_path in models_to_test.items():
        if not os.path.exists(model_path):
            print(f"Brak modelu {model_path}")
            continue

        print(f"Testowanie {model_name}...")
        model = YOLO(model_path)

        ious = {'Car': [], 'Pedestrian': []}
        false_positives = {'Car': 0, 'Pedestrian': 0}
        total_time = 0.0

        images_processed = 0

        for img_path in tqdm(images_paths, desc=f"Przetwarzanie {model_name}"):
            img_name = os.path.basename(img_path)
            res_img_path = os.path.join(output_dir, f"{model_name}_{img_name}")

            if os.path.exists(res_img_path):
                continue

            label_name = img_name.replace('.jpg', '.txt')
            label_path = os.path.join('labels', label_name)

            truths = read_kitti_labels(label_path)

            start_time = time.time()
            # COCO classes: 0 - person, 2 - car
            res = model(img_path, classes=[0, 2], verbose=False)[0]
            end_time = time.time()
            total_time += (end_time - start_time)

            # Save visualization
            res_img = res.plot()
            cv2.imwrite(os.path.join(output_dir, f"{model_name}_{img_name}"), res_img)

            preds = {'Car': [], 'Pedestrian': []}
            for box in res.boxes:
                cls_id = int(box.cls[0].item())
                bbox = box.xyxy[0].tolist()

                if cls_id == 0:
                    preds['Pedestrian'].append(bbox)
                elif cls_id == 2:
                    preds['Car'].append(bbox)

            for cls in ['Car', 'Pedestrian']:
                matched_preds = set()

                for t_box in truths[cls]:
                    best_iou = 0
                    best_pred_idx = -1

                    for p_idx, p_box in enumerate(preds[cls]):
                        if p_idx in matched_preds:
                            continue
                        iou = calculate_iou(t_box, p_box)
                        if iou > best_iou:
                            best_iou = iou
                            best_pred_idx = p_idx

                    if best_iou > 0.5:
                        ious[cls].append(best_iou)
                        matched_preds.add(best_pred_idx)
                    else:
                        ious[cls].append(0)

                false_positives[cls] += len(preds[cls]) - len(matched_preds)

            images_processed += 1

        avg_time = total_time / images_processed if images_processed > 0 else 0
        avg_iou_car = np.mean(ious['Car']) if ious['Car'] else 0
        avg_iou_ped = np.mean(ious['Pedestrian']) if ious['Pedestrian'] else 0

        results[model_name] = {
            'Avg IoU Car': avg_iou_car,
            'Avg IoU Pedestrian': avg_iou_ped,
            'False Positives Car': false_positives['Car'],
            'False Positives Pedestrian': false_positives['Pedestrian']
        }
        fps_results[model_name] = avg_time

    print("\n--- Podsumowanie wyników ---")
    df = pd.DataFrame(results).T
    print(df)
    print("\nŚredni czas inferencji (sekundy/obraz):")
    for m, t in fps_results.items():
        print(f"{m}: {t:.4f} s")

    print(f"\nPorównanie YOLO11x vs YOLO26x:")
    if 'YOLO11x' in results and 'YOLO26x' in results:
        print(
            f"YOLO11x - IoU Car: {results['YOLO11x']['Avg IoU Car']:.4f}, IoU Ped: {results['YOLO11x']['Avg IoU Pedestrian']:.4f}")
        print(
            f"YOLO26x - IoU Car: {results['YOLO26x']['Avg IoU Car']:.4f}, IoU Ped: {results['YOLO26x']['Avg IoU Pedestrian']:.4f}")

    yolo26_models = [m for m in results.keys() if 'YOLO26' in m]

    if yolo26_models:
        # Plot IoU Car
        plt.figure()
        plt.bar(yolo26_models, [results[m]['Avg IoU Car'] for m in yolo26_models], color='blue')
        plt.title('Średnie IoU - Klasa Car (YOLO26)')
        plt.ylabel('IoU')
        plt.savefig(os.path.join(output_dir, 'iou_car.png'))

        # Plot IoU Pedestrian
        plt.figure()
        plt.bar(yolo26_models, [results[m]['Avg IoU Pedestrian'] for m in yolo26_models], color='orange')
        plt.title('Średnie IoU - Klasa Pedestrian (YOLO26)')
        plt.ylabel('IoU')
        plt.savefig(os.path.join(output_dir, 'iou_pedestrian.png'))

        # Examples of bad inference (FP / FN)
        print(f"\nPrzykłady błędnej inferencji zostały zapisane w katalogu {output_dir}")


if __name__ == '__main__':
    main()
