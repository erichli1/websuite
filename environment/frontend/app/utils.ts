export const TASKS = ["click", "type", "select"] as const;
type TaskType = (typeof TASKS)[number];

export const CLICK_TESTS = ["button", "link"] as const;
export type ClickTestType = (typeof CLICK_TESTS)[number];
