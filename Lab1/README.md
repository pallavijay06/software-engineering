# Lab 1 – Requirements Engineering & UML Use-Case Modelling

## Problem Statement

**Digital Campus Library Reservation Gateway**

A modern university library system to search physical ISBN catalogs, manage dynamic holding queues for borrowed copies, automate holding notifications, and track overdue fine transactions.

## Lab Objective

To elicit and document functional and nonfunctional requirements from the given scenario and translate them into a UML use-case diagram and a use-case flow specification.

## Actors

- Student Member
- Head Librarian
- Payment Gateway

## Use Cases

- **UC-01:** Search ISBN Catalog
- **UC-02:** Place Book Hold
- **UC-03:** Manage Holding Queue
- **UC-04:** Send Holding Notification
- **UC-05:** Track Overdue Fine Transactions

## UML Relationships

- `<<include>>` – Place Book Hold includes Check Hold Eligibility
- `<<extend>>` – Notify Student of Book Availability extends Send Holding Notification

## Core Use Case

**UC-02 – Place Book Hold**

The use-case flow specifies the preconditions, postconditions, main success scenario, and alternate flow for placing a book hold.

## Deliverables

1. Requirements Table
2. UML Use-Case Diagram
3. Use-Case Flow Specification

## Files

- `PES1UG24CS313_RequirementsLAB1.pdf` – Requirements Table
- `PES1UG24CS313_Lab1UML.pdf` – UML Use-Case Diagram
- `PES1UG24CS313_SELAB1.pdf` – Use-Case Flow Specification