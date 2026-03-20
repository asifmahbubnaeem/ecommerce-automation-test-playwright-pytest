Status Badge: 
[![CI](https://github.com/asifmahbubnaeem/ecommerce-automation-test-playwright-pytest/actions/workflows/ci.yml/badge.svg)](https://github.com/asifmahbubnaeem/ecommerce-automation-test-playwright-pytest/actions/workflows/ci.yml)


## Overview

This repository contains a production-grade UI test automation framework for the SauceDemo e-commerce site, implemented in **Python + Playwright** with **pytest** as the test runner.

The focus is on clean architecture, maintainability, and realistic engineering practices: configuration and test data management, Page Object Model, fixtures, reporting, and CI/CD via GitHub Actions.

## Framework Choice & Rationale

- **Python + Playwright + pytest**:
  - Playwright provides fast, reliable, auto-waiting browser automation with rich debugging (traces, screenshots, videos).
  - Python and pytest are widely adopted in QA teams, with excellent plugin ecosystems and simple, expressive test syntax.
  - The stack is well-suited for parallel execution and CI environments.
- **Alternatives considered**:
  - **Selenium**: very mature and flexible, but more verbose and requires more manual wait handling.
  - **Cypress**: great Developer Experience for JS ecosystems, but focused on Chrome-family browsers and JavaScript; less aligned with a Python-centric QA stack.

Considering robust architecture, flakiness handling,  CI integration : Python + Playwright + pytest strikes the best balance between reliability, speed, and readability.
