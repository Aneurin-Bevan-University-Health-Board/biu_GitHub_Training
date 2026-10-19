![BIU Logo](../links%20and%20logos/BIU%20LOGO.png) ![DDAT Logo](../links%20and%20logos/DDAT%20Logo.png)

---

# Setup and Access (Complete Before the Training Day)

**Time needed**: 30–45 minutes  
**Who**: Every participant  
**Goal**: Arrive on the day signed in to GitHub, able to open a Codespace. Optionally, access to the **ndr-hb-abuhb-academy** Google Cloud project, and a GitHub personal access token (PAT) if your trainer asks for one.

> We use **GitHub Enterprise Cloud** through the ABUHB organisation. This is not the free personal GitHub plan, so some features in this training (protected branches on private repositories, Copilot Business, Codespaces controls, Advanced Security) only work inside the organisation. Do all training work with your organisation account.

> **ndr-hb-abuhb-academy** is a Google Cloud (GCP) project that the training lead sets up for this course, with a group of the participants as members. The course itself is GitHub-first: you work in a Codespace and need nothing installed locally.

> Items marked **[CONFIRM]** are details the training lead must fill in before the day, because they depend on how the project is set up.

---

## 1. Checklist

A printable version is in the [Participant Pack](../Participant_Pack/02_Getting_Started_Checklist.md).

```text
□ GitHub account created and linked to your NHS Wales email
□ Added to the ABUHB organisation (Azure AD group ABB_BIU_GitHub_Users)
□ Single sign-on (SSO) works when you open the organisation
□ Two-factor authentication switched on
□ Codespaces opens (Section 5): this is your workspace for the whole day
□ Optional: added to the ndr-hb-abuhb-academy access group (Section 6, for the SQL extension)
□ Personal access token created and stored safely, if your trainer asks for one (Section 4)
□ Optional: Git, GitHub Desktop and VS Code installed on your own computer
```

---

## 2. Get Access to the Organisation

1. Create or sign in to your GitHub account at <https://github.com>. Use your NHS Wales email, or add it to your account under **Settings → Emails**.
2. Make sure you are in the Azure AD group `ABB_BIU_GitHub_Users`. Ask your line manager or the GitHub admin team if you are not sure.
3. Open the organisation: <https://github.com/Aneurin-Bevan-University-Health-Board>. If asked, choose **Single sign-on** and sign in with your NHS Wales account.
4. Turn on two-factor authentication under **Settings → Password and authentication**. Keep your recovery codes somewhere safe.
5. Open the training repository **[CONFIRM: repository name and URL]**. If you cannot see it, contact the admin team.

**Stuck?** Email the GitHub admin team at `ABB.BIU.GitHub.Admin@nhswales365.onmicrosoft.com` with your GitHub username. New repositories need an approved **HALO ticket** and are created by the admin team.

---

## 3. Tools: Codespaces First

The training uses **GitHub Codespaces**: VS Code in your browser, with Git and Python already set up and signed in to your GitHub account. You do not need to install anything.

| Tool | Needed? | Notes |
|------|---------|-------|
| A modern web browser | Yes | For github.com and Codespaces |
| GitHub Codespaces | Yes | Opened from the repository page; see Section 5 |
| Git, VS Code, GitHub Desktop | Optional | Only if you want to work on your own computer |

If you do install Git locally, tell it who you are (once per computer):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.nhs.wales"
```

Use the same email address you have added to GitHub.

---

## 4. Create a Personal Access Token (PAT)

A PAT is like a password for a single job. Git and other tools use it to prove who you are when they connect to GitHub, and to services that need a GitHub token. A Codespace signs you in automatically, so create a token only if your trainer asks for one (for example to connect a tool outside a Codespace). You create it, you control its power, and you can revoke it at any time.

### 4.1 Create a fine-grained token (recommended)

1. On GitHub, click your profile picture, then **Settings**.
2. Scroll to **Developer settings** (bottom of the left menu) → **Personal access tokens** → **Fine-grained tokens**.
3. Click **Generate new token**.
4. **Token name**: `github-training`.
5. **Expiration**: choose the shortest that covers the training, for example 30 days.
6. **Resource owner**: choose the ABUHB organisation (`Aneurin-Bevan-University-Health-Board`). If it is not listed, the organisation must allow fine-grained tokens: ask the admin team.
7. **Repository access**: choose **Only select repositories** and pick the training repository.
8. **Permissions** (repository): set only what you need.

   | Permission | Access |
   |------------|--------|
   | Contents | Read and write |
   | Pull requests | Read and write |
   | Issues | Read and write |
   | Metadata | Read-only (always on) |

9. Click **Generate token**. If the organisation requires approval, the token shows as pending until an owner approves it: tell the admin team.
10. **Copy the token now.** GitHub shows it only once.

### 4.2 If you must use a classic token

Only if the project needs it **[CONFIRM]**:

1. **Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic)**.
2. Tick `repo` only. Set a short expiry.
3. After generating, click **Configure SSO** next to the token and **Authorize** the ABUHB organisation. Without this, the token is refused with a 403 or "SAML enforcement" error.

### 4.3 Store the token safely

- Save it in the password manager approved for your team, **or** let the Git credential manager store it (below).
- **Never** put it in code, a notebook, a README, an issue, a pull request, a chat message or a Copilot prompt.
- Do not email it or save it in a shared folder.

### 4.4 Use the token

**With Git on your own computer (optional).** Clone the training repository. When Git asks for a password, paste the token (the username is your GitHub username). The Git Credential Manager saves it so you are not asked again:

```bash
git clone https://github.com/Aneurin-Bevan-University-Health-Board/<repository>.git
```

**With GitHub Desktop and VS Code (optional tools).** Both sign in through your browser, so they normally do not need the token.

**In a Codespace (Session 8).** Codespaces signs you in automatically. If a tool needs the token, add it as a Codespaces secret, never in a file:

1. **Settings → Codespaces → Secrets → New secret**.
2. Name it `ACADEMY_TOKEN`, paste the value, and select the training repository.
3. In the Codespace it appears as the environment variable `ACADEMY_TOKEN`.

### 4.5 Rotate and revoke

- Tokens expire. Create a new one before the old one ends.
- If a token is ever exposed (pasted in the wrong place, committed, shared), **revoke it immediately**: Settings → Developer settings → Personal access tokens → your token → **Delete**. Then tell the admin team.

---

## 5. Test Your Setup: Open a Codespace

1. Open the training repository on github.com and check that you can see the **participants** folder and your own folder, named `firstname-lastname`.
2. Choose **Code → Codespaces → Create codespace on main**.
3. A VS Code editor should open in the browser within a minute or two. Open the terminal (`` Ctrl+` ``) and run `git status`. You should see `On branch main` and `nothing to commit`.
4. You can stop the Codespace afterwards (**Codespaces: Stop Current Codespace** in the Command Palette). You will open it again on the day.

If you have Git installed locally you can also test with a clone:

```bash
git clone https://github.com/Aneurin-Bevan-University-Health-Board/<repository>.git
```

---

## 6. Optional: Google Cloud Project ndr-hb-abuhb-academy

**This section is optional.** The training day works without it. It is only needed for the SQL extension at the end of Session 9 and the BigQuery demos.

The training lead creates this GCP project and a Google group for participants. Access to the project is granted to the group, not to individuals.

1. The training lead adds your NHS Wales account to the group **[CONFIRM: group name]**.
2. Sign in to the Google Cloud console at <https://console.cloud.google.com> with your NHS Wales account and select the project **ndr-hb-abuhb-academy**.
3. Check that you can see the project **[CONFIRM: the role the group has, and what participants do in the project on the day]**.

> Real patient data stays in the Secure Data Environment. This academy project is for training only and holds synthetic data.

**GitHub and the project.** **[CONFIRM: how GitHub connects to the project, for example a deployment or a secret that uses a token, with the exact URL, variable name and test command.]**

---

## 7. Common Problems

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| 404 on the organisation or repository | Not yet a member, or SSO not completed | Complete SSO; ask the admin team to check the group |
| (Optional) Cannot see the ndr-hb-abuhb-academy project | Not yet in the Google group | Ask the training lead to add you |
| Codespaces will not start | Not enabled for you or the repository | Ask the admin team |
| 403 or "SAML enforcement" on push | Classic token not authorised for SSO | Configure SSO on the token and authorise it |
| "Authentication failed" | Wrong password or expired token | Paste the token, not your GitHub password; create a new token |
| Cannot push | Fine-grained token lacks Contents write | Edit the token permissions or create a new one |

---

## 8. Rules for the Day

- **Synthetic data only.** Never put real patient data in GitHub, Codespaces, issues or Copilot prompts.
- No tokens, passwords or secrets in any file.
- Real data stays in the Secure Data Environment. Code moves to the data, never the reverse.

*Setup and Access | GitHub Training Package*
