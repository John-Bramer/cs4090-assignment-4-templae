Feature: Task Management
  As a user
  I want to manage my to-do tasks
  So I can organize my work effectively

  Background:
    Given I start with an empty task list

  @add
  Scenario: Add a new task with details
    When I add a task "Buy milk" with:
      | Field    | Value     |
      | Priority | High      |
      | Category | Groceries |
      | Due Date | Tomorrow  |
    Then I should see "Buy milk" in my tasks
    And it should have priority "High"
    And it should belong to category "Groceries"

  @complete
  Scenario: Mark a task as completed
    Given I have a task "Write report" in my list
    When I mark "Write report" as completed
    Then the task should show as completed

  @filter
  Scenario: Filter tasks by priority
    Given I have these tasks:
      | Title       | Priority |
      | Urgent fix  | High     |
      | Read book   | Low      |
    When I filter by "High" priority
    Then I should only see "Urgent fix"

  @delete
  Scenario: Delete an existing task
    Given I have a task "Old task" in my list
    When I delete "Old task"
    Then it should not appear in my tasks

  @overdue
  Scenario: View overdue tasks
    Given I have a task "Pay bills" due yesterday
    When I view overdue tasks
    Then I should see "Pay bills" in the overdue list