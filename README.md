# Parent Portal Security Pipeline

## Overview
This project integrates **Claude 3.5 Sonnet** and **SonarQube** into a Jenkins pipeline to perform dual-layer security analysis on the Parent Portal Flask app.

## How it works
1. **SonarQube** performs Static Application Security Testing (SAST).
2. **Claude AI** performs semantic code review for logic-based vulnerabilities.
3. **Quality Gate** stops the build if security scores are below "Production Ready".

## Setup
1. Create a `.env` file on your EC2 with `CLAUDE_API_KEY`.
2. Ensure Jenkins has the `CLAUDE_API_KEY` credential stored.
