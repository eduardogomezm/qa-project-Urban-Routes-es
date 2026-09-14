Sprint9 Urban Routes Automation Project 

This repository represents Sprint 8 of my QA Engineering journey — building an end-to-end automation suite for the Urban Routes web application using Python, Selenium WebDriver, Pytest, and the Page Object Model (POM).

🚕 Automated Test Scope

This project covers the full flow of ordering a taxi in the Urban Routes app:

Setting pickup & drop-off addresses
Selecting the Supportive plan (with conditional check to avoid redundant clicks)
Entering and verifying phone number (via retrieve_phone_code() helper)
Adding a credit card (handling CVV/Link button edge case)
Writing a driver comment
Ordering blanket & handkerchiefs (state verification)
Ordering 2 ice creams
Ordering a taxi with Supportive tariff and verifying the car search modal

🛠 Tech Stack

Python 3.13
Selenium WebDriver
Pytest
ChromeDriver
Page Object Model (POM)
Git + GitHub
