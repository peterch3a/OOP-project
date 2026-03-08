
# OzZoo Simulator  
A real‑time, command‑driven zoo management simulation built with Python.

OzZoo is a modular, object‑oriented simulation where animals, visitors, enclosures, food systems, and special events interact in a continuously updating world. A background simulation thread drives the zoo’s behaviour while the user interacts through a rich command‑line interface with auto‑completion.

---

## Table of Contents
- Overview
- Features
- Architecture Breakdown
- Design Principles
- Simulation Loop
- Project Structure
- Getting Started
- Developer Guide
- Extending the System
- License

---

## Overview
OzZoo models a small but dynamic zoo ecosystem. Animals have happiness, habitat needs, and breeding behaviour. Visitors move through the zoo, react to what they see, and influence the zoo’s economy. Enclosures get dirty, food supplies run low, and random events can dramatically change the state of the zoo.

The simulation runs in real time, updating every few seconds, while the user interacts through a command‑line interface powered by `prompt_toolkit`.

---

## Features
- Real‑time simulation loop running in a background thread
- Rich CLI with auto‑completion and categorized commands
- Modular OOP architecture with clear separation of concerns
- Animal species with unique behaviours and habitat requirements
- Enclosure capacity, cleanliness, and upgrade mechanics
- Visitor movement, happiness, donations, and exit logic
- Food inventory and feeding system
- Random special events that affect animals, visitors, food, and budget
- Extensible design for new species, events, commands, or systems

---

## Architecture Breakdown

### Zoo (Core Orchestrator)
The `Zoo` class coordinates all major systems:
- Animal lifecycle (happiness, feeding, breeding, death)
- Enclosure cleanliness and capacity
- Visitor behaviour and economy
- Food inventory
- Special events
- Budget management

It exposes a clean API used by the CLI.

---

### Animals (Domain Model)
Defined in `animal.py`, the animal hierarchy uses inheritance and polymorphism:

```
Animal (abstract)
 ├── Mammal
 │    └── Marsupial
 │         ├── Koala
 │         └── Kangaroo
 └── Bird
      └── WedgeTailedEagle
```

Each species defines:
- Required habitat  
- Preferred food  
- Happiness gain from feeding  
- Sound  
- Breeding behaviour  

---

### Enclosures
Enclosures manage:
- Habitat type  
- Capacity and upgrades  
- Cleanliness  
- Animal assignment  

They implement the `ICleanable` interface.

---

### Visitors
Visitors:
- Move randomly  
- View enclosures  
- Donate or leave based on animal happiness  
- Deteriorate over time  

They are the primary source of income.

---

### Food System
Food objects track:
- Type (meat/leaves)
- Quantity

The zoo automatically feeds animals each update cycle.

---

### Manager (Economy)
The `Manager` class encapsulates the zoo’s budget. All spending and income flow through this object.

---

### Special Events
Events are polymorphic and easy to extend. Examples:
- Happy Day  
- Generous Donation  
- Visitor Festival  
- Disaster  
- Food Depletion  

Each event implements `apply(zoo)`.

---

### Command Interface
The CLI (`command.py`) provides:
- Auto‑completion for commands and arguments
- Categorized help menu
- Error handling
- Command routing via `do_<command>` methods

This module is the UI layer and does not contain simulation logic.

---

### Game Entry Point
`game.py`:
- Creates the Zoo and Command objects
- Starts the simulation thread
- Runs the CLI loop

---

## Design Principles

### Single Responsibility
Each class models one concept: Animal, Enclosure, Visitor, Food, Manager, etc.

### Encapsulation
Critical state (happiness, cleanliness, budget) is protected behind properties.

### Polymorphism
Animals and events use abstract base classes to enforce consistent interfaces.

### Loose Coupling
Modules interact through well‑defined APIs rather than deep interdependencies.

### Real‑Time Simulation
A background thread updates the world independently of user input.

### CLI‑First Interaction
The command interface is cleanly separated from simulation logic.

---

## Simulation Loop

Every 3 seconds, the zoo performs:

1. **Animal updates**  
   Happiness deterioration, habitat penalties, death removal.

2. **Enclosure updates**  
   Cleanliness decay and its impact on animals.

3. **Visitor updates**  
   Happiness changes, movement, viewing reactions, donations.

4. **Breeding**  
   Species‑specific breeding logic based on happiness and counters.

5. **Feeding**  
   Animals consume food and gain happiness.

6. **Visitor entry**  
   Ticket price affects acceptance probability.

7. **Special events**  
   3% chance per cycle.

8. **Cleanup**  
   Remove exited visitors.

This deterministic order makes debugging predictable.

---

## Project Structure

```
/project
│
├── animal.py
├── enclosure.py
├── visitor.py
├── food.py
├── manager.py
├── special_events.py
├── exceptions.py
├── interfaces.py
├── zoo.py
├── command.py
├── game.py
└── README.md
```

---

## Getting Started

### Requirements
- Python 3.10+
- prompt_toolkit

Install dependencies:

```
pip install prompt_toolkit
```

### Running the Program

```
python game.py
```

You will see:

- A welcome message  
- A categorized list of commands  
- A live simulation running in the background  

Use TAB to auto‑complete commands and arguments.

---

## Developer Guide

### Adding a New Animal Species
1. Subclass `Animal` or an appropriate intermediate class.
2. Define:
   - `preferred_food`
   - `happiness_gain`
   - `required_habitat`
   - `make_sound()`
3. Add the species to the mapping in `Zoo.add_animal()`.
4. Add species name to auto‑completion in `ZooCompleter`.

---

### Adding a New Special Event
1. Subclass `SpecialEvent`.
2. Implement `apply(self, zoo)`.
3. Add an instance to `Zoo._special_events`.

---

### Adding a New Command
1. Add a method `do_<command>(self, arg)` in `Command`.
2. Add a docstring for help menu.
3. Optionally decorate with `@command_category`.
4. Add argument suggestions in `ZooCompleter`.

---

### Adding a New Cleanable Structure
1. Implement `ICleanable`.
2. Add cleaning logic.
3. Add a command to clean it if needed.

---

## License
This project is provided as-is for educational and development purposes.
