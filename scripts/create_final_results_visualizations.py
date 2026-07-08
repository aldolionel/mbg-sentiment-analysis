"""Create thesis-ready final result visualizations and visual reports."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "mbg_labeled_sample_1000.csv"
COMPARISON_TABLE_PATH = (
    PROJECT_ROOT / "outputs" / "reports" / "16_final_modeling_comparison_table.csv"
)
COMPARISON_SUMMARY_PATH = (
    PROJECT_ROOT / "outputs" / "reports" / "16_final_modeling_comparison_summary.json"
)
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

LABEL_DISTRIBUTION_BAR_PATH = FIGURES_DIR / "16_final_label_distribution.png"
LABEL_DISTRIBUTION_PIE_PATH = FIGURES_DIR / "16_final_label_distribution_pie.png"
MACRO_F1_PATH = FIGURES_DIR / "16_model_comparison_macro_f1.png"
ACCURACY_VS_MACRO_F1_PATH = (
    FIGURES_DIR / "16_model_comparison_accuracy_vs_macro_f1.png"
)
LINEAR_SVM_IMPROVEMENT_PATH = FIGURES_DIR / "16_linear_svm_improvement.png"
NEGATIVE_CLASS_PATH = FIGURES_DIR / "16_negative_class_performance_tuned_svm.png"
VISUAL_REPORT_PATH = REPORTS_DIR / "17_final_visual_results_report.md"
NARRATIVE_DRAFT_PATH = REPORTS_DIR / "17_thesis_results_narrative_draft.md"

LABEL_ORDER = ["negatif", "netral", "positif"]
LABEL_COLORS = {
    "negatif": "#C44E52",
    "netral": "#8172B2",
    "positif": "#55A868",
}
MODEL_COLOR_BASELINE = "#6B7280"
MODEL_COLOR_TUNED = "#2F6F9F"


def read_json(path: Path) -> dict[str, Any]:
    """Read a required JSON file."""
    if not path.exists():
        raise FileNotFoundError(f"Required input not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> pd.DataFrame:
    """Read a required CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"Required input not found: {path}")
    return pd.read_csv(path)


def prepare_output_dirs() -> None:
    """Ensure report and figure directories exist."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def apply_common_style() -> None:
    """Apply readable matplotlib defaults for thesis figures."""
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#333333",
            "axes.labelcolor": "#222222",
            "xtick.color": "#222222",
            "ytick.color": "#222222",
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.labelsize": 11,
            "legend.fontsize": 10,
        }
    )


def save_current_figure(path: Path) -> None:
    """Save current matplotlib figure as a high-resolution PNG."""
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def label_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Return label counts and percentages in a stable order."""
    counts = df["label"].value_counts().reindex(LABEL_ORDER)
    distribution = counts.rename("count").reset_index()
    distribution.columns = ["label", "count"]
    distribution["percentage"] = distribution["count"] / len(df) * 100
    return distribution


def create_label_distribution_bar(distribution: pd.DataFrame) -> None:
    """Create the final label distribution bar chart."""
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    bars = ax.bar(
        distribution["label"],
        distribution["count"],
        color=[LABEL_COLORS[label] for label in distribution["label"]],
        edgecolor="#333333",
        linewidth=0.8,
    )
    ax.set_title("Distribusi Label Sentimen pada Sampel Berlabel")
    ax.set_xlabel("Label Sentimen")
    ax.set_ylabel("Jumlah Data")
    ax.set_ylim(0, max(distribution["count"]) * 1.18)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)

    for bar, (_, row) in zip(bars, distribution.iterrows()):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(distribution["count"]) * 0.025,
            f"{int(row['count'])}\n({row['percentage']:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    save_current_figure(LABEL_DISTRIBUTION_BAR_PATH)


def create_label_distribution_pie(distribution: pd.DataFrame) -> None:
    """Create the final label distribution pie chart."""
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    labels = [
        f"{row.label}\n{int(row.count)} ({row.percentage:.1f}%)"
        for row in distribution.itertuples(index=False)
    ]
    ax.pie(
        distribution["count"],
        labels=labels,
        colors=[LABEL_COLORS[label] for label in distribution["label"]],
        startangle=90,
        counterclock=False,
        wedgeprops={"edgecolor": "white", "linewidth": 1.2},
        textprops={"fontsize": 10},
    )
    ax.set_title("Proporsi Label Sentimen pada Sampel Berlabel")
    ax.axis("equal")
    save_current_figure(LABEL_DISTRIBUTION_PIE_PATH)


def create_macro_f1_comparison(comparison_df: pd.DataFrame) -> None:
    """Create model comparison by macro F1."""
    sorted_df = comparison_df.sort_values("f1_macro", ascending=True)
    colors = [
        MODEL_COLOR_TUNED if group == "Tuned SVM" else MODEL_COLOR_BASELINE
        for group in sorted_df["model_group"]
    ]

    fig, ax = plt.subplots(figsize=(9.2, 5.8))
    bars = ax.barh(sorted_df["model_name"], sorted_df["f1_macro"], color=colors)
    ax.set_title("Perbandingan Model Berdasarkan Macro F1")
    ax.set_xlabel("Macro F1")
    ax.set_xlim(0, min(1.0, max(sorted_df["f1_macro"]) + 0.12))
    ax.grid(axis="x", color="#DDDDDD", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)

    for bar in bars:
        ax.text(
            bar.get_width() + 0.008,
            bar.get_y() + bar.get_height() / 2,
            f"{bar.get_width():.4f}",
            va="center",
            fontsize=9,
        )
    save_current_figure(MACRO_F1_PATH)


def create_accuracy_vs_macro_f1(comparison_df: pd.DataFrame) -> None:
    """Create grouped comparison for accuracy and macro F1."""
    plot_df = comparison_df.sort_values("f1_macro", ascending=False).reset_index(drop=True)
    x_positions = range(len(plot_df))
    width = 0.36

    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    acc_positions = [x - width / 2 for x in x_positions]
    f1_positions = [x + width / 2 for x in x_positions]
    acc_bars = ax.bar(
        acc_positions,
        plot_df["accuracy"],
        width=width,
        label="Akurasi",
        color="#8C8C8C",
    )
    f1_bars = ax.bar(
        f1_positions,
        plot_df["f1_macro"],
        width=width,
        label="Macro F1",
        color=MODEL_COLOR_TUNED,
    )

    ax.set_title("Perbandingan Akurasi dan Macro F1")
    ax.set_ylabel("Nilai Metrik")
    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(plot_df["model_name"], rotation=35, ha="right")
    ax.set_ylim(0, 0.9)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    ax.legend()

    for bars in [acc_bars, f1_bars]:
        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.012,
                f"{bar.get_height():.3f}",
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=90,
            )
    save_current_figure(ACCURACY_VS_MACRO_F1_PATH)


def create_linear_svm_improvement(summary: dict[str, Any]) -> None:
    """Create improvement chart from baseline Linear SVM to tuned LinearSVC."""
    improvement = summary["linear_svm_improvement"]
    labels = ["Linear SVM\nBaseline", "Tuned LinearSVC"]
    values = [
        improvement["baseline_linear_svm_f1_macro"],
        improvement["tuned_linearsvc_f1_macro"],
    ]

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    bars = ax.bar(labels, values, color=[MODEL_COLOR_BASELINE, MODEL_COLOR_TUNED])
    ax.plot(labels, values, color="#222222", marker="o", linewidth=1.8)
    ax.set_title("Peningkatan Macro F1 Setelah Tuning Linear SVM")
    ax.set_ylabel("Macro F1")
    ax.set_ylim(0.64, max(values) + 0.05)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.006,
            f"{value:.4f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax.annotate(
        f"+{improvement['percentage_point_improvement']:.2f} poin",
        xy=(1, values[1]),
        xytext=(0.55, values[1] + 0.032),
        arrowprops={"arrowstyle": "->", "color": "#222222"},
        fontsize=10,
    )
    save_current_figure(LINEAR_SVM_IMPROVEMENT_PATH)


def create_negative_class_performance(summary: dict[str, Any]) -> None:
    """Create negative-class precision/recall/F1 chart for tuned SVMs."""
    display_names = {
        "tuned_linearsvc": "Tuned\nLinearSVC",
        "tuned_svc_linear": "SVC Linear",
        "tuned_svc_rbf": "SVC RBF",
    }
    rows = []
    for experiment, metrics in summary["negative_class_performance"].items():
        rows.append(
            {
                "model": display_names.get(experiment, experiment),
                "Precision": metrics["precision"],
                "Recall": metrics["recall"],
                "F1": metrics["f1-score"],
            }
        )
    perf_df = pd.DataFrame(rows)

    x_positions = range(len(perf_df))
    width = 0.24
    metric_specs = [
        ("Precision", "#4C78A8", -width),
        ("Recall", "#F58518", 0),
        ("F1", "#54A24B", width),
    ]

    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    for metric, color, offset in metric_specs:
        positions = [x + offset for x in x_positions]
        bars = ax.bar(positions, perf_df[metric], width=width, label=metric, color=color)
        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.012,
                f"{bar.get_height():.3f}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

    ax.set_title("Performa Kelas Negatif pada Model SVM Tuning")
    ax.set_ylabel("Nilai Metrik")
    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(perf_df["model"])
    ax.set_ylim(0, 0.68)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    ax.legend()
    save_current_figure(NEGATIVE_CLASS_PATH)


def write_visual_report(
    summary: dict[str, Any],
    distribution: pd.DataFrame,
) -> None:
    """Write concise visual results report."""
    best = summary["best_overall_model"]
    improvement = summary["linear_svm_improvement"]
    lines = [
        "# 17 Final Visual Results Report",
        "",
        "## Scope",
        "This report documents thesis-ready visualization assets created from existing final modeling comparison outputs. No models were retrained, no labels were changed, and no raw files were modified.",
        "",
        "## Input Files",
        f"- `{DATA_PATH}`",
        f"- `{COMPARISON_TABLE_PATH}`",
        f"- `{COMPARISON_SUMMARY_PATH}`",
        "",
        "## Output Figures",
        f"- `{LABEL_DISTRIBUTION_BAR_PATH}`",
        f"- `{LABEL_DISTRIBUTION_PIE_PATH}`",
        f"- `{MACRO_F1_PATH}`",
        f"- `{ACCURACY_VS_MACRO_F1_PATH}`",
        f"- `{LINEAR_SVM_IMPROVEMENT_PATH}`",
        f"- `{NEGATIVE_CLASS_PATH}`",
        "- existing final model confusion matrix: `outputs/figures/15_confusion_matrix_tuned_linearsvc.png`",
        "",
        "## Key Numbers",
        f"- total rows: {summary['dataset']['total_rows']}",
        "- final label distribution:",
    ]
    for row in distribution.itertuples(index=False):
        lines.append(f"  - {row.label}: {int(row.count)} ({row.percentage:.2f}%)")
    lines.extend(
        [
            f"- best model: {summary['recommendation']}",
            f"- best macro F1: {best['metrics']['f1_macro']:.4f}",
            "- improvement from baseline Linear SVM: "
            f"{improvement['absolute_improvement']:.4f} "
            f"({improvement['percentage_point_improvement']:.2f} percentage points)",
            "",
            "## Catatan Interpretasi Gambar",
            "### Distribusi Label",
            "Grafik distribusi label menunjukkan bahwa sampel berlabel didominasi oleh kelas `netral` dan `positif`, sedangkan kelas `negatif` memiliki proporsi paling kecil. Kondisi ini menjelaskan mengapa evaluasi model perlu menekankan macro F1, bukan hanya akurasi.",
            "",
            "### Perbandingan Model",
            "Grafik perbandingan macro F1 memperlihatkan bahwa model hasil tuning SVM berada pada peringkat teratas. Tuned LinearSVC menjadi model terbaik berdasarkan macro F1 pada data uji.",
            "",
            "### Peningkatan Tuning SVM",
            "Grafik peningkatan Linear SVM menunjukkan adanya kenaikan macro F1 setelah tuning hyperparameter. Peningkatan ini mendukung pemilihan Tuned LinearSVC sebagai model yang direkomendasikan.",
            "",
            "### Keterbatasan Kelas Negatif",
            "Grafik performa kelas negatif menunjukkan bahwa F1 kelas `negatif` masih lebih rendah dibandingkan performa keseluruhan model. Hal ini perlu dibahas sebagai keterbatasan karena jumlah data negatif relatif sedikit.",
            "",
            "## Recommendation for Thesis",
            "- Include `16_final_label_distribution.png` early in Bab Hasil dan Pembahasan to establish class imbalance.",
            "- Follow with `16_model_comparison_macro_f1.png` and `16_model_comparison_accuracy_vs_macro_f1.png` to compare model performance.",
            "- Present `16_linear_svm_improvement.png` when discussing the effect of SVM tuning.",
            "- Include `15_confusion_matrix_tuned_linearsvc.png` and `16_negative_class_performance_tuned_svm.png` for final model interpretation and limitations.",
            "- Suggested order: label distribution, unified model comparison, SVM tuning improvement, final confusion matrix, negative-class limitation.",
            f"",
            f"_Generated at: {datetime.now().isoformat(timespec='seconds')}_",
        ]
    )
    VISUAL_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_narrative_draft(summary: dict[str, Any]) -> None:
    """Write Indonesian thesis-ready narrative draft."""
    dataset = summary["dataset"]
    best = summary["best_overall_model"]
    improvement = summary["linear_svm_improvement"]
    negative = summary["negative_class_performance"]["tuned_linearsvc"]
    lines = [
        "# 17 Thesis Results Narrative Draft",
        "",
        "## Distribusi Label",
        f"Dataset yang digunakan pada tahap pemodelan terdiri dari {dataset['total_rows']} data berlabel yang merupakan sampel dari hasil crawling media sosial terkait MBG. Label pada dataset ini diperoleh melalui proses AI-assisted labeling dengan adjudication/manual review, sehingga hasil analisis perlu dipahami sebagai gambaran pada sampel berlabel, bukan sebagai klaim universal mengenai opini publik.",
        "",
        f"Distribusi label menunjukkan bahwa kelas `netral` berjumlah {dataset['label_distribution']['netral']} data ({dataset['label_percentage']['netral']:.2f}%), kelas `positif` berjumlah {dataset['label_distribution']['positif']} data ({dataset['label_percentage']['positif']:.2f}%), dan kelas `negatif` berjumlah {dataset['label_distribution']['negatif']} data ({dataset['label_percentage']['negatif']:.2f}%). Ketidakseimbangan ini menjadi pertimbangan penting dalam pemilihan metrik evaluasi model.",
        "",
        "## Perbandingan Model Baseline",
        "Pada eksperimen baseline, beberapa model klasifikasi klasik dibandingkan menggunakan representasi fitur TF-IDF, yaitu Multinomial Naive Bayes, Logistic Regression, Linear SVM, dan RBF SVM. Perbandingan ini bertujuan memberikan gambaran awal mengenai performa model sebelum tuning lebih lanjut pada keluarga SVM.",
        "",
        "Karena distribusi label tidak seimbang, macro F1 digunakan sebagai metrik utama. Macro F1 lebih sesuai dibandingkan akurasi saja karena memberikan bobot yang sama pada setiap kelas, termasuk kelas `negatif` yang jumlah datanya paling sedikit.",
        "",
        "## Hasil Tuning SVM",
        f"Tuning SVM dilakukan pada LinearSVC, SVC dengan kernel linear, dan SVC dengan kernel RBF. Hasil tuning menunjukkan bahwa Tuned LinearSVC memperoleh macro F1 sebesar {best['metrics']['f1_macro']:.4f} pada data uji, dengan akurasi sebesar {best['metrics']['accuracy']:.4f}.",
        "",
        f"Dibandingkan baseline Linear SVM, tuning meningkatkan macro F1 dari {improvement['baseline_linear_svm_f1_macro']:.4f} menjadi {improvement['tuned_linearsvc_f1_macro']:.4f}. Peningkatan absolut sebesar {improvement['absolute_improvement']:.4f} atau sekitar {improvement['percentage_point_improvement']:.2f} percentage points menunjukkan bahwa pemilihan parameter berpengaruh terhadap performa model SVM.",
        "",
        "## Pemilihan Model Terbaik",
        f"Berdasarkan macro F1 sebagai metrik utama, model yang direkomendasikan adalah Tuned LinearSVC + TF-IDF. Model ini dipilih karena menghasilkan macro F1 tertinggi di antara model baseline dan model SVM hasil tuning, yaitu {best['metrics']['f1_macro']:.4f}.",
        "",
        "Pemilihan Tuned LinearSVC juga sejalan dengan fokus penelitian pada model SVM. Dengan kombinasi TF-IDF dan tuning hyperparameter, model ini memberikan performa yang lebih baik dibandingkan Linear SVM baseline dan juga melampaui Logistic Regression baseline pada macro F1.",
        "",
        "## Keterbatasan",
        f"Meskipun Tuned LinearSVC memberikan performa terbaik secara keseluruhan, performa pada kelas `negatif` masih perlu dicermati. Pada model Tuned LinearSVC, F1 untuk kelas `negatif` adalah {negative['f1-score']:.4f}, dengan recall {negative['recall']:.4f}. Nilai ini menunjukkan bahwa model masih mengalami tantangan dalam mengenali sentimen negatif secara konsisten.",
        "",
        "Keterbatasan lain adalah ukuran dataset berlabel yang berjumlah 1.000 sampel dari kumpulan data crawling yang lebih besar. Selain itu, proses pelabelan bersifat AI-assisted dengan adjudication/manual review, sehingga validasi manual yang lebih luas dapat menjadi arah pengembangan penelitian berikutnya.",
        "",
        "## Ringkasan Temuan",
        "Secara keseluruhan, hasil pemodelan menunjukkan bahwa pendekatan TF-IDF + Tuned LinearSVC merupakan model yang paling sesuai untuk digunakan sebagai model akhir pada tahap pembahasan hasil. Macro F1 digunakan sebagai dasar pemilihan karena dataset memiliki distribusi label yang tidak seimbang.",
        "",
        "Temuan ini mendukung penggunaan SVM yang telah dituning sebagai pendekatan klasifikasi sentimen MBG pada sampel berlabel. Namun, interpretasi hasil tetap perlu dibatasi pada dataset sampel yang digunakan dan tidak boleh digeneralisasikan sebagai opini publik secara keseluruhan.",
    ]
    NARRATIVE_DRAFT_PATH.write_text("\n".join(lines), encoding="utf-8")


def create_final_visualizations() -> None:
    """Create all final visualizations and reports."""
    prepare_output_dirs()
    apply_common_style()

    df = read_csv(DATA_PATH)
    comparison_df = read_csv(COMPARISON_TABLE_PATH)
    summary = read_json(COMPARISON_SUMMARY_PATH)
    distribution = label_distribution(df)

    create_label_distribution_bar(distribution)
    create_label_distribution_pie(distribution)
    create_macro_f1_comparison(comparison_df)
    create_accuracy_vs_macro_f1(comparison_df)
    create_linear_svm_improvement(summary)
    create_negative_class_performance(summary)
    write_visual_report(summary, distribution)
    write_narrative_draft(summary)

    print(f"Saved figure: {LABEL_DISTRIBUTION_BAR_PATH}")
    print(f"Saved figure: {LABEL_DISTRIBUTION_PIE_PATH}")
    print(f"Saved figure: {MACRO_F1_PATH}")
    print(f"Saved figure: {ACCURACY_VS_MACRO_F1_PATH}")
    print(f"Saved figure: {LINEAR_SVM_IMPROVEMENT_PATH}")
    print(f"Saved figure: {NEGATIVE_CLASS_PATH}")
    print(f"Saved report: {VISUAL_REPORT_PATH}")
    print(f"Saved narrative draft: {NARRATIVE_DRAFT_PATH}")


def main() -> None:
    """CLI entrypoint."""
    create_final_visualizations()


if __name__ == "__main__":
    main()
