import numpy as np
import os
import csv


def load_reference_patterns(database_folder="database"):
    """
    Load all .xy or .csv reference patterns from the database folder.
    Each file should have two columns: 2theta, intensity
    Returns a list of dicts: {name, two_theta, intensity}
    """
    patterns = []

    for filename in os.listdir(database_folder):
        if filename.endswith(".xy") or filename.endswith(".csv"):
            filepath = os.path.join(database_folder, filename)
            two_theta = []
            intensity = []

            with open(filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") or line == "":
                        continue  # skip comments and blank lines
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            two_theta.append(float(parts[0]))
                            intensity.append(float(parts[1]))
                        except ValueError:
                            continue

            if two_theta:
                patterns.append({
                    "name": filename.replace(".xy", "").replace(".csv", ""),
                    "two_theta": np.array(two_theta),
                    "intensity": np.array(intensity)
                })

    return patterns


def normalize(intensity_array):
    """Normalize intensity to 0-1 range."""
    min_val = np.min(intensity_array)
    max_val = np.max(intensity_array)
    if max_val - min_val == 0:
        return intensity_array
    return (intensity_array - min_val) / (max_val - min_val)


def resample(two_theta, intensity, common_grid):
    """Resample a pattern onto a common 2theta grid for comparison."""
    return np.interp(common_grid, two_theta, intensity,
                     left=0, right=0)


def match_pattern(input_two_theta, input_intensity, reference_patterns, top_n=5):
    """
    Compare input pattern against all references using cosine similarity.
    Returns top N matches sorted by score.
    """
    common_grid = np.linspace(10, 80, 1000)

    input_resampled = resample(input_two_theta, input_intensity, common_grid)
    input_normalized = normalize(input_resampled)

    results = []

    for ref in reference_patterns:
        ref_resampled = resample(ref["two_theta"], ref["intensity"], common_grid)
        ref_normalized = normalize(ref_resampled)

        # Cosine similarity
        dot_product = np.dot(input_normalized, ref_normalized)
        norm_input = np.linalg.norm(input_normalized)
        norm_ref = np.linalg.norm(ref_normalized)

        if norm_input == 0 or norm_ref == 0:
            score = 0.0
        else:
            score = dot_product / (norm_input * norm_ref)

        results.append({
            "name": ref["name"],
            "score": round(float(score), 4),
            "two_theta": ref["two_theta"],
            "intensity": ref["intensity"]
        })

    # Sort by score, highest first
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]


if __name__ == "__main__":
    print("matcher.py loaded successfully.")
