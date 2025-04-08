"""
Benchmark utilities for the ProventraCore library.
"""
import json
import time
from typing import Dict, List, Any, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, roc_curve, auc

from proventra_core import GuardService


# Add a NumPy-compatible JSON encoder
class NumpyEncoder(json.JSONEncoder):
    """JSON encoder that handles NumPy data types."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def calculate_detection_metrics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate detection metrics from benchmark results.
    
    Args:
        results: List of result dictionaries with actual and predicted labels
        
    Returns:
        Dictionary with detection metrics
    """
    y_true = [r["is_attack"] for r in results]
    y_pred = [r["detected_as_attack"] for r in results]
    risk_scores = [r["risk_score"] for r in results]
    
    # Calculate basic metrics
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    
    # Calculate derived metrics
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    # Calculate risk score metrics
    attack_scores = [score for score, is_attack in zip(risk_scores, y_true) if is_attack]
    benign_scores = [score for score, is_attack in zip(risk_scores, y_true) if not is_attack]
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "avg_attack_risk_score": np.mean(attack_scores) if attack_scores else 0,
        "avg_benign_risk_score": np.mean(benign_scores) if benign_scores else 0,
        "risk_score_std": np.std(risk_scores) if risk_scores else 0
    }


def calculate_sanitization_metrics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate sanitization metrics from benchmark results.
    
    Args:
        results: List of result dictionaries with sanitization information
        
    Returns:
        Dictionary with sanitization metrics
    """
    # Filter for attack cases
    attack_results = [r for r in results if r["is_attack"]]
    
    # Calculate metrics
    successfully_sanitized = sum(1 for r in attack_results if r["successfully_sanitized"])
    sanitization_success_rate = successfully_sanitized / len(attack_results) if attack_results else 0
    
    return {
        "sanitization_attempts": len(attack_results),
        "successful_sanitizations": successfully_sanitized,
        "sanitization_success_rate": sanitization_success_rate
    }


def calculate_performance_metrics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate performance metrics from benchmark results.
    
    Args:
        results: List of result dictionaries with timing information
        
    Returns:
        Dictionary with performance metrics
    """
    processing_times = [r["processing_time"] for r in results]
    
    return {
        "avg_processing_time": np.mean(processing_times),
        "median_processing_time": np.median(processing_times),
        "min_processing_time": np.min(processing_times),
        "max_processing_time": np.max(processing_times),
        "std_processing_time": np.std(processing_times)
    }


def analyze_by_category(results: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    """
    Analyze benchmark results by input category.
    
    Args:
        results: List of result dictionaries
        
    Returns:
        Dictionary with metrics for each category
    """
    categories = {}
    
    for result in results:
        category = result["category"]
        if category not in categories:
            categories[category] = {
                "count": 0, 
                "correct": 0, 
                "processing_time": []
            }
        
        categories[category]["count"] += 1
        if result["is_attack"] == result["detected_as_attack"]:
            categories[category]["correct"] += 1
        categories[category]["processing_time"].append(result["processing_time"])
    
    # Calculate metrics for each category
    category_metrics = {}
    for category, data in categories.items():
        category_metrics[category] = {
            "accuracy": data["correct"] / data["count"],
            "avg_processing_time": np.mean(data["processing_time"]),
            "sample_count": data["count"]
        }
    
    return category_metrics


def analyze_by_difficulty(results: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    """
    Analyze benchmark results by difficulty level.
    
    Args:
        results: List of result dictionaries
        
    Returns:
        Dictionary with metrics for each difficulty level
    """
    difficulties = {}
    
    for result in results:
        difficulty = result["difficulty"]
        if difficulty not in difficulties:
            difficulties[difficulty] = {
                "count": 0, 
                "correct": 0, 
                "processing_time": []
            }
        
        difficulties[difficulty]["count"] += 1
        if result["is_attack"] == result["detected_as_attack"]:
            difficulties[difficulty]["correct"] += 1
        difficulties[difficulty]["processing_time"].append(result["processing_time"])
    
    # Calculate metrics for each difficulty
    difficulty_metrics = {}
    for difficulty, data in difficulties.items():
        difficulty_metrics[difficulty] = {
            "accuracy": data["correct"] / data["count"],
            "avg_processing_time": np.mean(data["processing_time"]),
            "sample_count": data["count"]
        }
    
    return difficulty_metrics


def generate_plots(results: List[Dict[str, Any]], output_dir: str) -> None:
    """
    Generate and save plots from benchmark results.
    
    Args:
        results: List of result dictionaries
        output_dir: Directory to save plots
    """
    # Prepare data for plots
    df = pd.DataFrame(results)
    y_true = df["is_attack"]
    y_pred = df["detected_as_attack"]
    
    # 1. Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    plt.xticks([0, 1], ['Benign', 'Attack'])
    plt.yticks([0, 1], ['Benign', 'Attack'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    
    # Add text annotations to the confusion matrix
    thresh = cm.max() / 2
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/confusion_matrix.png")
    plt.close()
    
    # 2. ROC Curve
    if len(set(y_true)) > 1:  # Only calculate ROC if we have both classes
        fpr, tpr, _ = roc_curve(y_true, y_pred)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc="lower right")
        plt.savefig(f"{output_dir}/roc_curve.png")
        plt.close()
    
    # 3. Performance by Category
    category_metrics = analyze_by_category(results)
    categories = list(category_metrics.keys())
    accuracy_values = [metrics["accuracy"] for metrics in category_metrics.values()]
    time_values = [metrics["avg_processing_time"] for metrics in category_metrics.values()]
    
    # Sort by accuracy
    sorted_indices = np.argsort(accuracy_values)
    sorted_categories = [categories[i] for i in sorted_indices]
    sorted_accuracy = [accuracy_values[i] for i in sorted_indices]
    
    plt.figure(figsize=(12, 8))
    plt.barh(sorted_categories, sorted_accuracy, color='skyblue')
    plt.xlabel('Accuracy')
    plt.title('Accuracy by Input Category')
    plt.xlim([0, 1])
    plt.tight_layout()
    plt.savefig(f"{output_dir}/accuracy_by_category.png")
    plt.close()
    
    # 4. Performance by Difficulty
    difficulty_metrics = analyze_by_difficulty(results)
    difficulties = ["easy", "medium", "hard"]
    difficulty_accuracy = [difficulty_metrics.get(d, {"accuracy": 0})["accuracy"] for d in difficulties]
    
    plt.figure(figsize=(10, 6))
    plt.bar(difficulties, difficulty_accuracy, color='lightgreen')
    plt.xlabel('Difficulty Level')
    plt.ylabel('Accuracy')
    plt.title('Accuracy by Difficulty Level')
    plt.ylim([0, 1])
    plt.savefig(f"{output_dir}/accuracy_by_difficulty.png")
    plt.close()
    
    # 5. Processing Time Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df["processing_time"], bins=20, color='lightblue', edgecolor='black')
    plt.xlabel('Processing Time (seconds)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Processing Times')
    plt.savefig(f"{output_dir}/processing_time_distribution.png")
    plt.close()


def generate_report(results: List[Dict[str, Any]], output_file: str) -> Dict[str, Any]:
    """
    Generate and save a comprehensive benchmark report.
    
    Args:
        results: List of result dictionaries
        output_file: Path to save the report
        
    Returns:
        Dictionary with all metrics
    """
    # Calculate various metrics
    detection_metrics = calculate_detection_metrics(results)
    sanitization_metrics = calculate_sanitization_metrics(results)
    performance_metrics = calculate_performance_metrics(results)
    category_metrics = analyze_by_category(results)
    difficulty_metrics = analyze_by_difficulty(results)
    
    # Prepare a comprehensive report
    report = {
        "summary": {
            "total_samples": len(results),
            "attack_samples": sum(1 for r in results if r["is_attack"]),
            "benign_samples": sum(1 for r in results if not r["is_attack"]),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "detection": detection_metrics,
        "sanitization": sanitization_metrics,
        "performance": performance_metrics,
        "by_category": category_metrics,
        "by_difficulty": difficulty_metrics,
        "failed_cases": [
            {
                "text": r["text"],
                "category": r["category"],
                "difficulty": r["difficulty"],
                "is_attack": r["is_attack"],
                "detected_as_attack": r["detected_as_attack"]
            }
            for r in results if r["is_attack"] != r["detected_as_attack"]
        ]
    }
    
    # Save the report as JSON with custom encoder for NumPy types
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2, cls=NumpyEncoder)
    
    return report


def run_benchmark_on_guard(
    guard_service: GuardService,
    test_data: List[Dict[str, Any]],
    output_dir: str
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Run a comprehensive benchmark on a GuardService instance.
    
    Args:
        guard_service: The GuardService instance to benchmark
        test_data: List of test cases
        output_dir: Directory to save benchmark results and plots
        
    Returns:
        Tuple of (detailed results list, summary report)
    """
    results = []
    
    print(f"Starting benchmark with {len(test_data)} test cases...")
    
    for i, item in enumerate(test_data):
        print(f"Processing item {i+1}/{len(test_data)}...")
        
        try:
            # Measure processing time
            start_time = time.time()
            analysis = guard_service.analyze_and_sanitize(item["text"])
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Record the result
            result = {
                "text": item["text"],
                "is_attack": item["is_attack"],
                "category": item["category"],
                "difficulty": item["difficulty"],
                "detected_as_attack": analysis.unsafe,
                "risk_score": analysis.risk_score,
                "successfully_sanitized": analysis.sanitized is not None if analysis.unsafe else None,
                "sanitized_text": analysis.sanitized,
                "sanitization_reason": analysis.sanitization_details.reason if analysis.sanitization_details else None,
                "processing_time": processing_time
            }
            
            results.append(result)
            
        except Exception as e:
            print(f"Error processing item {i+1}: {str(e)}")
            # Record the error
            results.append({
                "text": item["text"],
                "is_attack": item["is_attack"],
                "category": item["category"],
                "difficulty": item["difficulty"],
                "error": str(e),
                "detected_as_attack": None,
                "successfully_sanitized": None,
                "processing_time": 0
            })
    
    # Save detailed results with custom encoder for NumPy types
    with open(f"{output_dir}/detailed_results.json", "w") as f:
        json.dump(results, f, indent=2, cls=NumpyEncoder)
    
    # Generate summary report
    report = generate_report(results, f"{output_dir}/summary_report.json")
    
    # Generate plots
    try:
        generate_plots(results, output_dir)
    except Exception as e:
        print(f"Error generating plots: {str(e)}")
    
    return results, report 