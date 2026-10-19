# Training Deck: How the PowerPoint and Markdown Stay in Sync

The deck [`../GitHub_Training_Day.pptx`](../GitHub_Training_Day.pptx) and the session notes are **both generated from one file**:

**[`deck_content.yaml`](deck_content.yaml)**: every slide's title, headings, bullets, note and callout, plus each session's title, time, duration and file.

## Changing the training

1. Edit `deck_content.yaml` (slide wording, session times, adding or removing slides).
2. Run:

   ```bash
   pip install -r Training/slides/requirements.txt
   python Training/slides/build_deck.py
   ```

3. Commit the YAML **and** everything it regenerated.

The build:

| It updates | How |
|------------|-----|
| `Training/GitHub_Training_Day.pptx` | Rebuilt from `template.pptx` (the SDE Training Day style: navy title and section slides, white content slides) |
| `Training/0N_Session_N_*.md` | The **Slide Deck Content** block at the end of each file (between the `SLIDES:BEGIN` / `SLIDES:END` markers), the `Duration` and `Time` header lines, and the "Session N of M" footer |
| `README.md` and `Training/README.md` | The timetable table (between the `SESSIONS-TABLE` markers) |

**Do not hand-edit** the generated blocks. The detailed teaching notes elsewhere in each session file are hand-written and are not touched.

## Checking for drift

```bash
python Training/slides/build_deck.py --check
```

Changes nothing and exits with an error if the deck, a session file or a README no longer matches the YAML. The GitHub Action in `.github/workflows/deck-sync.yml` runs this on every pull request that touches the training, so a hand edit to the PowerPoint or to a generated block cannot be merged by accident.

> **Editing a slide directly in PowerPoint?** The next build will overwrite it. Make the change in the YAML instead. The check also flags the difference.

## Notes

- Slides with a lot of text automatically get a slightly smaller font; if a slide is too full the build stops and asks you to split it.
- Quote any bullet containing ` #` in the YAML (for example `"Closes #123"`), because YAML otherwise treats it as a comment. The build refuses unquoted ones.
- `template.pptx` is the SDE Training Day deck with its slides removed. Replace it to restyle the whole deck.
