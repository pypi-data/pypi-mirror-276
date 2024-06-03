from collections import defaultdict

def f1_score(y_true, y_pred, average='binary'):
    """
    Compute F1-score of the model.
    
    Parameters:
        y_true : array-like of shape (n_samples,)
            True labels.
        y_pred : array-like of shape (n_samples,)
            Predicted labels.
        average : str, default='binary'
            Averaging strategy to apply. Possible values are {'micro', 'macro', 'weighted', 'binary', None}.
            If None, return F1-score for each class.
    
    Returns:
        f1 : float or array of float
            F1-score(s).
    """
    if len(y_true) != len(y_pred):
        raise ValueError("Lengths of y_true and y_pred must be the same.")
    
    if average == 'binary':
        # Calculate true positives, false positives, and false negatives for binary classification
        tp = sum((true == 1) and (pred == 1) for true, pred in zip(y_true, y_pred))
        fp = sum((true == 0) and (pred == 1) for true, pred in zip(y_true, y_pred))
        fn = sum((true == 1) and (pred == 0) for true, pred in zip(y_true, y_pred))
        
        # Calculate precision and recall
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        
        # Calculate F1 score
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)
    
    elif average in {'micro', 'macro', 'weighted', None}:
        # Calculate true positives, false positives, and false negatives for multi-class classification
        tp = defaultdict(int)
        fp = defaultdict(int)
        fn = defaultdict(int)
        
        for true, pred in zip(y_true, y_pred):
            if true == pred:
                tp[true] += 1
            else:
                fp[pred] += 1
                fn[true] += 1
        
        if average == 'micro':
            # Calculate micro-averaged precision and recall
            micro_tp = sum(tp.values())
            micro_fp = sum(fp.values())
            micro_fn = sum(fn.values())
            
            precision = micro_tp / (micro_tp + micro_fp) if micro_tp + micro_fp > 0 else 0
            recall = micro_tp / (micro_tp + micro_fn) if micro_tp + micro_fn > 0 else 0
        else:  # macro, weighted, or None
            # Calculate precision and recall for each class
            precision = {}
            recall = {}
            for label in set(y_true + y_pred):
                tp_label = tp[label]
                fp_label = fp[label]
                fn_label = fn[label]
                precision[label] = tp_label / (tp_label + fp_label) if tp_label + fp_label > 0 else 0
                recall[label] = tp_label / (tp_label + fn_label) if tp_label + fn_label > 0 else 0
            
            if average == 'macro':
                # Calculate macro-averaged precision and recall
                precision = sum(precision.values()) / len(precision) if len(precision) > 0 else 0
                recall = sum(recall.values()) / len(recall) if len(recall) > 0 else 0
            elif average == 'weighted':
                # Calculate weighted-averaged precision and recall
                weights = defaultdict(int)
                for label in y_true:
                    weights[label] += 1
                precision = sum(precision[label] * weights[label] for label in precision) / len(y_true) if len(y_true) > 0 else 0
                recall = sum(recall[label] * weights[label] for label in recall) / len(y_true) if len(y_true) > 0 else 0
            else:  # average == None
                # Return F1 score for each class
                return {label: 2 * (precision[label] * recall[label]) / (precision[label] + recall[label]) if precision[label] + recall[label] > 0 else 0.0 for label in precision}
        
        # Calculate F1 score for micro-averaged precision and recall
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)
    
    else:
        raise ValueError("Invalid value for 'average'.")
