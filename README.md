# minji-kim-portfolio

Personal portfolio site for Minji Kim. Live at [minji-kim-portfolio.vercel.app](https://minji-kim-portfolio.vercel.app).

Plain HTML and CSS, deployed on Vercel with no build step.

## Pages

- `/` home: headline, selected projects, recent experience, writing
- `/projects/` all projects, each with its own page under `/projects/<slug>/`
- `/writing/` papers and posts, tagged Published Technical Paper, Blog, or Research/Policy Paper
- `/about/` experience, education, honors, courses, skills, CV
- `/cafes/` café guide

## Updating content

All text lives at the top of `build.py`.

1. Edit the lists there (projects, writing, experience, cafés, and so on).
2. Run `python3 build.py` to regenerate every page.
3. Commit the changed files and push.

Styles are in `style.css`. Images and the CV PDF are in `photo/`.
