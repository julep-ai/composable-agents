/**
 * Workflow and task management models
 * DBOS-backed durable execution state
 */

import "@typespec/rest";

using TypeSpec.Rest;

namespace JulepV2;

/**
 * Durable workflow definition
 * 
 * AIDEV-NOTE: workflow-model; DBOS workflow state
 * - Workflows persist state between steps
 * - Automatic recovery from failures
 * - Progress tracking and monitoring
 */
@resource("workflows")
model Workflow {
  @key
  @visibility("read")
  id: uuid;
  
  @doc("Workflow type identifier")
  type: string;
  
  @doc("Agent executing this workflow")
  agentId: uuid;
  
  @doc("Current workflow state")
  state: WorkflowState;
  
  @doc("Input parameters for the workflow")
  input: unknown;
  
  @doc("Current step being executed")
  currentStep?: string;
  
  @doc("Workflow execution result")
  result?: unknown;
  
  @doc("Error information if failed")
  error?: WorkflowError;
  
  @visibility("read")
  startedAt: utcDateTime;
  
  @visibility("read")
  completedAt?: utcDateTime;
}

enum WorkflowState {
  @doc("Workflow is waiting to start")
  pending: "PENDING",
  
  @doc("Workflow is currently executing")
  running: "RUNNING",
  
  @doc("Workflow completed successfully")
  completed: "COMPLETED",
  
  @doc("Workflow failed with error")
  failed: "FAILED",
  
  @doc("Workflow was cancelled")
  cancelled: "CANCELLED"
}

model WorkflowError {
  @doc("Error code for categorization")
  code: string;
  
  @doc("Human-readable error message")
  message: string;
  
  @doc("Step where error occurred")
  step?: string;
  
  @doc("Stack trace for debugging")
  stackTrace?: string;
}

/**
 * A2A Task for inter-agent collaboration
 * 
 * AIDEV-NOTE: task-model; multi-agent task coordination
 * - Tasks can be assigned to multiple agents
 * - Dependencies between tasks
 * - Progress tracking across agents
 */
@resource("tasks")
model Task {
  @key
  @visibility("read")
  id: uuid;
  
  @doc("Task title")
  title: string;
  
  @doc("Detailed task description")
  description: string;
  
  @doc("Required agent capabilities")
  requiredCapabilities: string[];
  
  @doc("Agents assigned to this task")
  assignedAgents: uuid[];
  
  @doc("Task priority")
  priority: TaskPriority;
  
  @doc("Current task state")
  state: TaskState;
  
  @doc("Task dependencies")
  dependencies?: uuid[];
  
  @visibility("read")
  createdAt: utcDateTime;
  
  @visibility("read")
  dueDate?: utcDateTime;
}

enum TaskPriority {
  urgent: "urgent",
  high: "high",
  normal: "normal",
  low: "low"
}

enum TaskState {
  created: "created",
  assigned: "assigned",
  inProgress: "in_progress",
  completed: "completed",
  failed: "failed"
}

// AIDEV-TODO: workflow-steps; define step execution model
// AIDEV-TODO: task-results; task completion and aggregation
// AIDEV-TODO: workflow-events; event streaming for monitoring