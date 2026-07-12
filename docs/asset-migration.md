# Getting the Enter360 assets onto GitHub

Goal: the Squarespace scrape of enter360.com, the personal portfolio site ZIP,
and the portfolio project folder all live in a **private** GitHub repo so any
Claude session (local or cloud) can work with them.

## 1. Create a private repo

From the machine that has the files (do NOT use the public `xcharron/xcharron`
profile repo — client work and site content shouldn't be public):

```bash
gh repo create xcharron/enter360-assets --private
# or create it at github.com/new, set Private
```

## 2. Recommended structure

```
enter360-assets/
├── squarespace-export/   # the AI-fetched index, content, and copy from enter360.com
├── personal-site/        # unzipped contents of the sheldoncharron.com pull
├── portfolio/            # the portfolio project folder
│   ├── rockspring/
│   ├── the-ranch/
│   ├── swfa/
│   └── ...
└── README.md             # what's here, where it came from, date pulled
```

## 3. The media problem (read before pushing)

GitHub hard-limits files to **100 MB** and repos get painful past a few GB.
Portfolio video/reels will blow past this. Options, in order of preference:

1. **Keep heavy media out of git.** Videos stay on Vimeo/YouTube/Drive/R2;
   the repo holds copy, structure, images, and a `media-index.md` linking out.
2. **Git LFS** for images/PDFs that must be versioned:
   `git lfs install && git lfs track "*.psd" "*.mp4"` — note LFS storage quotas.

Quick check before committing: `find . -size +90M` — anything it prints needs
option 1 or 2.

## 4. Push

```bash
cd /path/to/assembled/folder
git init && git add . && git commit -m "Import Enter360 + portfolio assets"
git branch -M main
git remote add origin git@github.com:xcharron/enter360-assets.git
git push -u origin main
```

## 5. Give Claude sessions access

In a cloud session, say "add the enter360-assets repo" (it gets added via
`add_repo`). Local Claude Code sessions just clone it.
