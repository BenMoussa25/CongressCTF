# CongressCTF
This repository contains a collection of CTF challenges designed for **The Congress CTF** and **The Beginners CTF**.

# CongressCTF Challenges Repository

This repository contains a collection of CTF challenges designed for **The Congress CTF** and **The Beginners CTF**. The challenges span multiple categories, including **web exploitation, cryptography, reverse engineering, forensics, and binary exploitation**. Each challenge includes:

- A brief description  
- Required files  
- Solver script  
- Setup instructions (if necessary)  

## 📌 Challenge Categories
```
Web Exploitation - Digital Forensics - Cryptography - Binary Exploitation - Reverse Engineering - Misc - Hardware
```

## 🚀 Repository & Contribution Rules

### 🛠️ Challenge Submission Process
- Clone the repository to your machine.
- Structure your challenge folder properly.
- Once you finish, make a **Pull Request (PR)** to the repo.
- For **Forensics** challenges, include private links to the files and MD5 checksum (**please do not push large files directly**).

### 📁 Challenge Folder Structure
```
[D] Is for Directory
[sD] Is for Sub-Directory
[F] Is for File
Please do not include them while naming your folders.

[D]challenge_name
    [sD]- challenge
    [sD]- solution
    [sD]- handout // contains zip or 7z archive with to-give source (redacted source code ...)
    [F]- challenge.yml
    [F]- compose.yml // for hostable challenges.
```

### 🔀 How to Make a Pull Request (PR)
**Work on your challenge in your branch first, then make a merge PR.**

1. Switch to your branch, add files, commit, and push:
```sh
git branch -M "challenge-name_category" # Example: InfiniteRumble_Misc
git add .
git commit -m "challenge"
git push origin challenge-name_category
```
2. Visit the repository on GitHub, and you’ll see a button **`Compare & Pull request`**.
3. Change the PR title to:
   ```
   (difficulty) category: challenge_name (author-name)
   ```
   Example: `(Easy) Misc: InfiniteRumble (Ouerfelli)`

## 🔥 Challenge Distribution
```
Binary Exploitation:
    bahae - buddurid
Web Exploitation:
    Mohamed Masmoudi - Enigma
    Mohamed Karrab - Karrab
    Jhinaoui Wassim - Chuuya
Reverse Engineering:
    Adem Hammadi - Gaaroura
    Jihed Kdiss - Jio
Digital Forensics:
    Hedi - Kakarot
    Mohamed Masmoudi - Enigma
Hardware:
    Adem Hammadi - Gaaroura
Misc:
    Hedi - Kakarot
    bahae - buddurid
    Adem Hammadi - Gaaroura
```

## 🎯 Goal
Minimum **10 challenges** per category.

## ⚡ Difficulty Levels
All levels, from **Easy** to **Insane**.

## ⏳ Time Duration
**12 Hours**

## 📅 Important Dates
**Congress CTF Date:** `26-27 April 2025, 08 PM`

**Deadline to Submit Challenges:** `20 April 2025, 11:59 PM`

