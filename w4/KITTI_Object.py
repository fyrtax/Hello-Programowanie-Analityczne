import glob
import os as os
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
from ultralytics import YOLO


# np.logical_and
# np.logical_or
# iou = np.sum(intersection) / np.sum(union) if np.sum(union) > 0 else 0
# Wykres obrazujący skuteczność sieci dla klasy Pedestrian
# (5 sieci YOLO - 5 słupków)
# Wykres obrazujący skuteczność sieci dla klasy Car
# 3. Profilowanie, czyli średni czas inferencji na zdjęcie
# false positives
# Napisać skrypt, który dokonuje ewaluacji sieci neuronowej YOLO 26 na podstawie danych KITTI
# Model: wszystkie wersje YOLO 26 + jedna wersja YOLO 11
# Funkcjonalność:
# • wczytywanie z plików tekstowych danych referencyjnych
# • zapisywanie wizualizacji wyników detekcji do katalogu z wynikami
# • obliczanie miary IoU w oparciu o dane referencyjne. Miarę IoU należy obliczyć niezależnie dla
# klas obiektów „Pedestrian” oraz „Car”.
# • profilowanie samej inferencji i obliczanie średniego czasu inferencji na obraz
# • *dodatkowo: wyznaczenie liczby „false positive” dla każdego testowanego modelu (funkcjonalność
# opcjonalna)
# Prezentacja:
# • wykresy obrazujące uzyskane miary IoU dla wszystkich modeli YOLO 26
# • porównanie wartości uzyskanych dla YOLO 11 vs YOLO 26 dla tego samego rodzaju modelu (nie
# musi być wykres, wystarczą same wartości)
# • przykłady błędnej inferencji dla wybranego modelu YOLO 26 w postaci wizualizacji YOLO. Należy
# pokazać zarówno przykład braku detekcji jak również przykład „false positive”
# jako obrazy do analizy to jest ich fragment gdzie numer zdjęcia to 4, 14, 24, 34 itp.
# yolo11x - porównanie z yolo26x


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
    SAVE_RESULT_IMAGES = False  # Przełącznik do kontrolowania czy zapisywać zdjęcia z wizualizacją

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

    # Obliczanie referencyjnej liczby obiektów we wszystkich przetwarzanych obrazach
    total_ground_truth_counts = {'Car': 0, 'Pedestrian': 0}
    for img_path in images_paths:
        img_name = os.path.basename(img_path)
        label_name = img_name.replace('.jpg', '.txt')
        label_path = os.path.join('labels', label_name)
        truths = read_kitti_labels(label_path)
        total_ground_truth_counts['Car'] += len(truths.get('Car', []))
        total_ground_truth_counts['Pedestrian'] += len(truths.get('Pedestrian', []))

    # Wczytywanie zdjęć do pamięci (aby zniwelować wpływ operacji I/O na czas inferencji)
    print("Wczytywanie obrazów do pamięci...")
    preloaded_images = {}
    for img_path in tqdm(images_paths, desc="Ładowanie zdjęć"):
        preloaded_images[img_path] = cv2.imread(img_path)

    results = {}
    fps_results = {}
    times_results = {}
    detections_counts = {}

    # Generowanie referencyjnych obrazków
    if SAVE_RESULT_IMAGES:
        print("Generowanie obrazków referencyjnych...")
        for img_path in tqdm(images_paths, desc="Referencyjne bbox"):
            img_name = os.path.basename(img_path)
            true_img_path = os.path.join(output_dir, f"true_{img_name}")

            if not os.path.exists(true_img_path):
                img = preloaded_images[img_path].copy()
                label_name = img_name.replace('.jpg', '.txt')
                label_path = os.path.join('labels', label_name)
                truths = read_kitti_labels(label_path)

                for cls_name, bboxes in truths.items():
                    color = (0, 255, 0) if cls_name == 'Car' else (255, 0, 0)
                    for box in bboxes:
                        x1, y1, x2, y2 = map(int, box)
                        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(img, cls_name, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                cv2.imwrite(true_img_path, img)

    for model_name, model_path in models_to_test.items():
        if not os.path.exists(model_path):
            print(f"Brak modelu {model_path}")
            continue

        print(f"Testowanie {model_name}...")
        model = YOLO(model_path)
        # Rozgrzewka modelu, by wyeliminować błąd pierwszego, długiego ładowania
        model(np.zeros((640, 640, 3), dtype=np.uint8), verbose=False)

        ious = {'Car': [], 'Pedestrian': []}
        true_positives = {'Car': 0, 'Pedestrian': 0}
        false_positives = {'Car': 0, 'Pedestrian': 0}
        false_negatives = {'Car': 0, 'Pedestrian': 0}
        times_per_image = []
        detected_counts = {'Car': 0, 'Pedestrian': 0}

        images_processed = 0

        for img_path in tqdm(images_paths, desc=f"Przetwarzanie {model_name}"):
            img_name = os.path.basename(img_path)
            res_img_path = os.path.join(output_dir, f"{model_name}_{img_name}")

            label_name = img_name.replace('.jpg', '.txt')
            label_path = os.path.join('labels', label_name)

            truths = read_kitti_labels(label_path)

            img_data = preloaded_images[img_path]

            start_time = time.time()
            # COCO classes: 0 - person, 2 - car
            res = model(img_data, classes=[0, 2], verbose=False)[0]
            end_time = time.time()

            # Zbieramy czas czystej inferencji YOLO (w ms) lub konwertujemy własny pomiar
            if hasattr(res, 'speed') and 'inference' in res.speed:
                inference_time = res.speed['inference']
            else:
                inference_time = (end_time - start_time) * 1000

            times_per_image.append(inference_time)

            if SAVE_RESULT_IMAGES and not os.path.exists(res_img_path):
                # Save visualization
                res_img = res.plot()
                cv2.imwrite(res_img_path, res_img)

            preds = {'Car': [], 'Pedestrian': []}
            for box in res.boxes:
                cls_id = int(box.cls[0].item())
                bbox = box.xyxy[0].tolist()

                if cls_id == 0:
                    preds['Pedestrian'].append(bbox)
                    detected_counts['Pedestrian'] += 1
                elif cls_id == 2:
                    preds['Car'].append(bbox)
                    detected_counts['Car'] += 1

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

                tp = len(matched_preds)
                fp = len(preds[cls]) - tp
                fn = len(truths[cls]) - tp

                true_positives[cls] += tp
                false_positives[cls] += fp
                false_negatives[cls] += fn

            images_processed += 1

        avg_iou_car = np.mean(ious['Car']) if ious['Car'] else 0
        avg_iou_ped = np.mean(ious['Pedestrian']) if ious['Pedestrian'] else 0

        # Car accuracy
        tp_car = true_positives['Car']
        fp_car = false_positives['Car']
        fn_car = false_negatives['Car']
        acc_car = tp_car / (tp_car + fp_car + fn_car) if (tp_car + fp_car + fn_car) > 0 else 0

        # Pedestrian accuracy
        tp_ped = true_positives['Pedestrian']
        fp_ped = false_positives['Pedestrian']
        fn_ped = false_negatives['Pedestrian']
        acc_ped = tp_ped / (tp_ped + fp_ped + fn_ped) if (tp_ped + fp_ped + fn_ped) > 0 else 0

        results[model_name] = {
            'Avg IoU Car': avg_iou_car,
            'Avg IoU Pedestrian': avg_iou_ped,
            'Accuracy Car': acc_car,
            'Accuracy Pedestrian': acc_ped,
            'False Positives Car': false_positives['Car'],
            'False Positives Pedestrian': false_positives['Pedestrian']
        }

        avg_time = np.mean(times_per_image) if len(times_per_image) > 0 else 0
        fps_results[model_name] = avg_time
        times_results[model_name] = times_per_image
        detections_counts[model_name] = detected_counts

    print("\n--- Podsumowanie wyników ---")
    df = pd.DataFrame(results).T
    print(df)
    print("\nŚredni czas inferencji (ms/obraz):")
    for m, t in fps_results.items():
        print(f"{m}: {t:.2f} ms")

    print(f"\nPorównanie YOLO11x vs YOLO26x:")
    if 'YOLO11x' in results and 'YOLO26x' in results:
        print(
            f"YOLO11x - IoU Car: {results['YOLO11x']['Avg IoU Car']:.4f}, IoU Ped: {results['YOLO11x']['Avg IoU Pedestrian']:.4f}, Acc Car: {results['YOLO11x']['Accuracy Car']:.4f}, Acc Ped: {results['YOLO11x']['Accuracy Pedestrian']:.4f}")
        print(
            f"YOLO26x - IoU Car: {results['YOLO26x']['Avg IoU Car']:.4f}, IoU Ped: {results['YOLO26x']['Avg IoU Pedestrian']:.4f}, Acc Car: {results['YOLO26x']['Accuracy Car']:.4f}, Acc Ped: {results['YOLO26x']['Accuracy Pedestrian']:.4f}")

    plot_models = list(results.keys())

    if plot_models:
        x = np.arange(len(plot_models))
        width = 0.35

        # Plot IoU Car
        plt.figure()
        plt.bar(plot_models, [results[m]['Avg IoU Car'] for m in plot_models], color='blue')
        plt.title('Średnie IoU - Klasa Car')
        plt.ylabel('IoU')
        plt.savefig(os.path.join(output_dir, 'iou_car.png'))

        # Plot IoU Pedestrian
        plt.figure()
        plt.bar(plot_models, [results[m]['Avg IoU Pedestrian'] for m in plot_models], color='orange')
        plt.title('Średnie IoU - Klasa Pedestrian')
        plt.ylabel('IoU')
        plt.savefig(os.path.join(output_dir, 'iou_pedestrian.png'))

        # Plot Accuracy (Car & Pedestrian)
        plt.figure()
        acc_car_vals = [results[m]['Accuracy Car'] for m in plot_models]
        acc_ped_vals = [results[m]['Accuracy Pedestrian'] for m in plot_models]

        plt.bar(x - width / 2, acc_car_vals, width, label='Car', color='#FF5733')
        plt.bar(x + width / 2, acc_ped_vals, width, label='Pedestrian', color='#FF3374')
        plt.title('Średnia pewność (Accuracy)')
        plt.ylabel('Accuracy')
        plt.xticks(x, plot_models)
        plt.legend()
        plt.savefig(os.path.join(output_dir, 'accuracy.png'))

        # Plot Time with Error Bars
        plt.figure()
        means = [np.mean(times_results[m]) for m in plot_models]
        stds = [np.std(times_results[m]) for m in plot_models]
        plt.bar(plot_models, means, yerr=stds, capsize=5, color='gray')
        plt.title('Średni czas inferencji')
        plt.ylabel('Czas [ms]')
        plt.savefig(os.path.join(output_dir, 'inference_time.png'))

        # Plot False Positives
        plt.figure()
        fp_car_vals = [results[m]['False Positives Car'] for m in plot_models]
        fp_ped_vals = [results[m]['False Positives Pedestrian'] for m in plot_models]

        plt.bar(x - width / 2, fp_car_vals, width, label='Car', color='red')
        plt.bar(x + width / 2, fp_ped_vals, width, label='Pedestrian', color='purple')
        plt.title('False Positives')
        plt.xticks(x, plot_models)
        plt.legend()
        plt.savefig(os.path.join(output_dir, 'false_positives.png'))

        # Plot Total Detections
        plt.figure()
        det_car = [detections_counts[m]['Car'] for m in plot_models]
        det_ped = [detections_counts[m]['Pedestrian'] for m in plot_models]

        plt.bar(x - width / 2, det_car, width, label='Car', color='green')
        plt.bar(x + width / 2, det_ped, width, label='Pedestrian', color='orange')

        # Linie oznaczające liczbę rzeczywistych obiektów z etykiet
        plt.axhline(y=total_ground_truth_counts['Car'], color='darkgreen', linestyle='--', label='Oczekiwane Car')
        plt.axhline(y=total_ground_truth_counts['Pedestrian'], color='saddlebrown', linestyle='--',
                    label='Oczekiwane Pedestrian')

        plt.title('Liczba wykrytych obiektów na klasę')
        plt.xticks(x, plot_models)
        plt.legend()
        plt.savefig(os.path.join(output_dir, 'detected_counts.png'))

        # Examples of bad inference (FP / FN)
        print(f"\nPrzykłady błędnej inferencji zostały zapisane w katalogu {output_dir}")


if __name__ == '__main__':
    main()
