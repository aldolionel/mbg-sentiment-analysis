# GitHub Publication Checklist

Use this checklist before pushing the repository to GitHub.

## Repository Content

- [ ] README complete and accurate.
- [ ] `requirements.txt` available.
- [ ] `automation_logs/` ignored by `.gitignore`.
- [ ] Raw data present if intended for publication.
- [ ] Final labeled dataset present.
- [ ] Reports present.
- [ ] Figures present.
- [ ] Notebooks present.
- [ ] Scripts compile.

## Hygiene

- [ ] No accidental secrets.
- [ ] No `.env` file.
- [ ] No cache files committed.
- [ ] No notebook checkpoints committed.
- [ ] Internal workflow transcript/log folders are ignored.

## Academic Transparency

- [ ] Methodology explains automatic labeling with AI-assisted review of flagged rows.
- [ ] README and docs do not claim manual adjudication or a human gold standard.
- [ ] Results are framed as analysis of sampled data, not universal public opinion.
- [ ] Limitations mention class imbalance and negative-class performance.

## GitHub Push Steps

```powershell
git status
git add README.md .gitignore docs scripts src notebooks data outputs requirements.txt LICENSE
git status
git commit -m "Prepare repository for GitHub publication"
git remote -v
git push origin main
```

If the default branch is `master`, replace `main` with `master`.
