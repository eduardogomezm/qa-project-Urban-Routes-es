# Sprint 9: Urban Routes Automated End-to-End Test Framework 🚕

A robust, maintainable, and scalable End-to-End (E2E) automated testing suite built for the **Urban Routes** web application. This project automates the critical path of the ride-hailing workflow, implementing industry-standard design patterns such as the **Page Object Model (POM)**, explicit synchronization strategies, and automated Chrome DevTools Protocol (CDP) network interception.

---

## 📌 Table of Contents
- [Overview & Functional Coverage](#-overview--functional-coverage)
- [Framework Architecture & Technical Design](#-framework-architecture--technical-design)
- [Repository Structure](#-repository-structure)
- [Prerequisites & System Requirements](#-prerequisites--system-requirements)
- [Framework Dependencies](#-framework-dependencies)
- [Setup & Installation](#-setup--installation)
- [Updating Dynamic Test Data](#-updating-dynamic-test-data)
- [Test Execution & Command Guide](#-test-execution--command-guide)

---

## 📖 Overview & Functional Coverage

The primary objective of this automated suite is to perform regression and validation testing on the complete order flow of **Urban Routes**. The suite covers end-to-end user scenarios from initial address entry to active vehicle search and driver assignment.

### Functional Scenarios Automated:
1. **Route Selection:** Setting "From" and "To" origin/destination addresses.
2. **Tariff Plan Selection:** Selecting the "Comfort" plan and verifying active state UI indicators.
3. **SMS Phone Authentication:** Requesting a verification code and intercepting performance logs to automatically extract and submit the pin.
4. **Payment Method Binding:** Adding a valid credit card (Card number + CVV) and linking it to the profile.
5. **Driver Communications:** Submitting custom instructions/comments for the driver.
6. **Additional Amenities:** Ordering trip extras including blankets/handkerchiefs and multiple ice cream items.
7. **Order Dispatch & Driver Modal:** Submitting the final ride request and asserting the visibility of the vehicle search modal and driver details overlay.

---

## 🏗️ Framework Architecture & Technical Design

This framework leverages clean architecture principles to maximize maintainability, readability, and test robustness:

```text
                                  +-----------------------+
                                  |     data.py / Env     |
                                  +-----------+-----------+
                                              |
                                              v
+-----------------------+         +-----------+-----------+         +-----------------------+
|  helpers.py (Utils &  | <-----> |   main.py (Test Suite)    | ------> |  pages.py (Page Object|
| Network Interceptors) |         |  Pytest / Assertions  |         |   Locators & Actions) |
+-----------------------+         +-----------------------+         +-----------+-----------+
                                                                                |
                                                                                v
                                                                    +-----------+-----------+
                                                                    |   Selenium WebDriver  |
                                                                    |     (Chrome Browser)  |
                                                                    +-----------------------+

📁 Repository Structure
qa-project-Urban-Routes-es/
│
├── pages.py            # Page Object Model encapsulating UI locators and page interactions
├── main.py             # Pytest test suite containing E2E test cases and assertions
├── helpers.py          # Utility functions for network interception & URL availability checks
├── data.py             # Test data constants (URLs, phone numbers, addresses, payment info)
├── requirements.txt    # Framework dependency declaration
└── README.md           # Technical documentation and execution guide


📋 Prerequisites & System Requirements

Before setting up the project locally, ensure your machine fulfills the following requirements:Python Runtime: Python 3.10+ (Tested and verified on Python 3.13.5).   
Browser: Google Chrome (Latest stable version)[cite: 5].WebDriver: Managed dynamically via Selenium Manager (built-in with Selenium 4+), eliminating the manual management of chromedriver binaries[cite: 5].

📦 Framework Dependencies

Plaintext
selenium>=4.0.0
pytest>=7.0.0

⚙️ Setup & Installation

Bash
git clone <repository_url>
cd qa-project-Urban-Routes-es


Install Dependencies

Bash
pip install --upgrade pip
pip install -r requirements.txt


🔄 Updating Dynamic Test Data

# data.py
urban_routes_url = '[https://cnt-66de97dc-e75d-495d-8ca3-869c41abe993.containerhub.tripleten-services.com?lng=es](https://cnt-66de97dc-e75d-495d-8ca3-869c41abe993.containerhub.tripleten-services.com?lng=es)'
address_from = 'East 2nd Street, 601'
address_to = '1300 1st St'
phone_number = '+1 123 123 12 12'
card_number, card_code = '1234 5678 9100', '111'
message_for_driver = 'Muéstrame el camino al museo'


🧪 Test Execution & Command Guide

Bash
pytest main.py

Bash
pytest -v -s main.py


