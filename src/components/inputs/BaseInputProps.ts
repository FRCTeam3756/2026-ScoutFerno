import { z } from "zod";

export const inputTypeSchema = z
  .enum([
    "text",
    "number",
    "boolean",
    "range",
    "select",
    "counter",
    "multi-counter",
    "timer",
    "multi-select",
    "image",
    "action-tracker",
    "TBA-team-and-robot",
    "TBA-match-number",
  ])
  .describe("The type of input");

export const inputBaseSchema = z.object({
  title: z.string().describe("The title of the input"),
  description: z.string().optional().describe("The description of the input"),
  type: inputTypeSchema,
  required: z.boolean().describe("Whether this input is required"),
  code: z.string().describe("A unique code for this input"),
  disabled: z.boolean().optional().describe("Whether this input is disabled"),
  formResetBehavior: z
    .enum(["reset", "preserve", "increment"])
    .default("reset")
    .describe("The behavior of this input when the form is reset"),

  });

export const stringInputSchema = inputBaseSchema.extend({
  type: z.literal("text"),
  min: z.number().optional().describe("The minimum length of the string"),
  max: z.number().optional().describe("The maximum length of the string"),
  defaultValue: z
    .string()
    .nullable()
    .optional()
    .default(null)
    .describe("The default value"),
});

export const numberInputSchema = inputBaseSchema.extend({
  type: z.literal("number"),
  min: z.number().optional().describe("The minimum value"),
  max: z.number().optional().describe("The maximum value"),
  defaultValue: z
    .number()
    .nullable()
    .optional()
    .default(null)
    .describe("The default value"),
});

export const selectInputSchema = inputBaseSchema.extend({
  type: z.literal("select"),
  choices: z.record(z.string()).optional().describe("The choices"),
  defaultValue: z
    .string()
    .nullable()
    .optional()
    .default(null)
    .describe("The default value. Must be one of the choices"),
});

export const multiSelectInputSchema = inputBaseSchema.extend({
  type: z.literal("multi-select"),
  choices: z.record(z.string()).optional().describe("The choices"),
  defaultValue: z.array(z.string()).optional().describe("The default value"),
});

export const counterInputSchema = inputBaseSchema.extend({
  type: z.literal("counter"),
  min: z.number().optional().describe("The minimum value"),
  max: z.number().optional().describe("The maximum value"),
  step: z.number().optional().describe("The step value").default(1),
  defaultValue: z.number().default(0).describe("The default value"),
});

export const multiCounterInputSchema = inputBaseSchema.extend({
  type: z.literal("multi-counter"),
  defaultValue: z.number().default(0).describe("The default value"),
});

export const rangeInputSchema = inputBaseSchema.extend({
  type: z.literal("range"),
  min: z.number().optional().describe("The minimum value"),
  max: z.number().optional().describe("The maximum value"),
  step: z.number().optional().describe("The step value").default(1),
  defaultValue: z.number().default(0).describe("The default value"),
});

export const booleanInputSchema = inputBaseSchema.extend({
  type: z.literal("boolean"),
  defaultValue: z.boolean().default(false).describe("The default value"),
});

export const timerInputSchema = inputBaseSchema.extend({
  type: z.literal("timer"),
  defaultValue: z.number().default(0).describe("The default value"),
  outputType: z
    .enum(["average", "list"])
    .default("average")
    .describe("The type of output to display in the scouting form"),
});

export const imageInputSchema = inputBaseSchema.extend({
  type: z.literal("image"),
  defaultValue: z
    .string()
    .nullable()
    .optional()
    .default(null)
    .describe("The URL to a statically hosted image"),
  width: z.number().optional().describe("The width of the image in pixels"),
  height: z.number().optional().describe("The height of the image in pixels"),
  alt: z.string().optional().describe("The alt text for the image"),
});

export const actionSchema = z.object({
  label: z.string().describe("The display label for this action button"),
  code: z
    .string()
    .describe("A unique code for this action (used in field names)"),
  icon: z
    .string()
    .optional()
    .describe(
      'Optional Lucide icon name (e.g., "fuel", "target"). See https://lucide.dev/icons',
    ),
});

export const tbaTeamAndRobotInputSchema = inputBaseSchema.extend({
  type: z.literal("TBA-team-and-robot"),
  defaultValue: z
    .object({
      team_number: z.number(),
      robot_position: z.string(),
    })
    .nullable()
    .optional()
    .default(null)
    .describe("The default team and robot position"),
});

export const tbaMatchNumberInputSchema = inputBaseSchema.extend({
  type: z.literal("TBA-match-number"),
  min: z.number().optional().describe("The minimum value"),
  max: z.number().optional().describe("The maximum value"),
  defaultValue: z.number().default(0).describe("The default value"),
});

export const sectionSchema = z.object({
  name: z.string(),
  fields: z.array(
    z.discriminatedUnion("type", [
      counterInputSchema,
      multiCounterInputSchema,
      stringInputSchema,
      numberInputSchema,
      selectInputSchema,
      multiSelectInputSchema,
      rangeInputSchema,
      booleanInputSchema,
      timerInputSchema,
      imageInputSchema,
      tbaTeamAndRobotInputSchema,
      tbaMatchNumberInputSchema,
    ]),
  ),
});

const shadcnColorSchema = z
  .string()
  .regex(/^(\d+(?:\.\d+)?)(?: (\d+(?:\.\d+)?)%)?(?: (\d+(?:\.\d+)?)%)?$/gm);

const shadcnRadiusSchema = z
  .string()
  .regex(/([0-9]*.[0-9]+rem)/)
  .optional();

export const colorSchemeSchema = z.object({
  background: shadcnColorSchema,
  foreground: shadcnColorSchema,
  card: shadcnColorSchema,
  card_foreground: shadcnColorSchema,
  popover: shadcnColorSchema,
  popover_foreground: shadcnColorSchema,
  primary: shadcnColorSchema,
  primary_foreground: shadcnColorSchema,
  secondary: shadcnColorSchema,
  secondary_foreground: shadcnColorSchema,
  muted: shadcnColorSchema,
  muted_foreground: shadcnColorSchema,
  accent: shadcnColorSchema,
  accent_foreground: shadcnColorSchema,
  destructive: shadcnColorSchema,
  destructive_foreground: shadcnColorSchema,
  border: shadcnColorSchema,
  input: shadcnColorSchema,
  ring: shadcnColorSchema,
  radius: shadcnRadiusSchema,
  chart_1: shadcnColorSchema,
  chart_2: shadcnColorSchema,
  chart_3: shadcnColorSchema,
  chart_4: shadcnColorSchema,
  chart_5: shadcnColorSchema,
});

export const configSchema = z.object({
  title: z
    .string()
    .describe(
      "The title of the scouting site. This will be displayed in the header and browser tab.",
    ),
  delimiter: z
    .string()
    .describe("The delimiter to use when joining the form data"),
  sections: z.array(sectionSchema),
});

export type InputTypes = z.infer<typeof inputTypeSchema>;

export type InputBase = z.infer<typeof inputBaseSchema>;
export type SelectInputData = z.infer<typeof selectInputSchema>;
export type MultiSelectInputData = z.infer<typeof multiSelectInputSchema>;
export type StringInputData = z.infer<typeof stringInputSchema>;
export type NumberInputData = z.infer<typeof numberInputSchema>;
export type CounterInputData = z.infer<typeof counterInputSchema>;
export type MultiCounterInputData = z.infer<typeof multiCounterInputSchema>;
export type RangeInputData = z.infer<typeof rangeInputSchema>;
export type BooleanInputData = z.infer<typeof booleanInputSchema>;
export type TimerInputData = z.infer<typeof timerInputSchema>;
export type ImageInputData = z.infer<typeof imageInputSchema>;
export type ActionData = z.infer<typeof actionSchema>;
export type TBATeamAndRobotInputData = z.infer<
  typeof tbaTeamAndRobotInputSchema
>;
export type TBAMatchNumberInputData = z.infer<typeof tbaMatchNumberInputSchema>;

export type InputPropsMap = {
  text: StringInputData;
  number: NumberInputData;
  boolean: BooleanInputData;
  range: RangeInputData;
  select: SelectInputData;
  "multi-select": MultiSelectInputData;
  counter: CounterInputData;
  "multi-counter": MultiCounterInputData;
  timer: TimerInputData;
  image: ImageInputData;
  "TBA-team-and-robot": TBATeamAndRobotInputData;
  "TBA-match-number": TBAMatchNumberInputData;
};

export type SectionProps = z.infer<typeof sectionSchema>;
export type Config = z.infer<typeof configSchema>;
export type ColorScheme = z.infer<typeof colorSchemeSchema>;
