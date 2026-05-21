import { produce } from "immer";
import { cloneDeep } from "lodash";
import configJson from "../assets/config.json";
import {
  ActionTrackerInputData,
  Config,
  configSchema,
  InputBase,
} from "../components/inputs/BaseInputProps";
import { MatchData } from "../types/matchData";
import { Result } from "../types/result";
import { supabase } from "../util/supabase";
import { createStore } from "./createStore";

export type { Result };

export const STORE_VERSION = 2;

function generateFieldValues(config: Config): { code: string; value: any }[] {
  const fieldValues: { code: string; value: any }[] = [];

  for (const section of config.sections) {
    for (const field of section.fields) {
      if (field.type === "action-tracker") {
        const actionField = field as ActionTrackerInputData;
        for (const action of actionField.actions) {
          fieldValues.push({
            code: `${field.code}_${action.code}_count`,
            value: 0,
          });
          fieldValues.push({
            code: `${field.code}_${action.code}_times`,
            value: "",
          });
        }
      } else {
        fieldValues.push({
          code: field.code,
          value: field.defaultValue,
        });
      }
    }
  }

  return fieldValues;
}

function getDefaultConfig(): Config {
  const config = configSchema.safeParse(configJson);
  if (!config.success) {
    console.error(config.error);
    throw new Error("Invalid config schema");
  }
  return config.data;
}

export function getConfig() {
  const configData = cloneDeep(useScoutFernoState.getState().formData);
  return configData;
}

export interface ScoutFernoState {
  formData: Config;
  fieldValues: { code: string; value: any }[];
  matchData?: MatchData[];
}

const initialState: ScoutFernoState = {
  formData: getDefaultConfig(),
  fieldValues: generateFieldValues(getDefaultConfig()),
};

export const useScoutFernoState = createStore<ScoutFernoState>(
  initialState,
  "scoutferno",
  {
    version: STORE_VERSION,
    migrate: (persistedState) => {
      const state = persistedState as Partial<ScoutFernoState>;

      if (!state.formData) {
        return { ...initialState, ...state };
      }

      const parsedConfig = configSchema.safeParse(state.formData);

      if (!parsedConfig.success) {
        return initialState;
      }

      return {
        ...initialState,
        ...state,
        formData: parsedConfig.data,
      } as ScoutFernoState;
    },
  },
);

export function resetToDefaultConfig() {
  useScoutFernoState.setState(initialState);
}

export async function fetchConfigFromURL(url: string): Promise<Result<void>> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(
        `Failed to fetch config from URL: ${response.statusText}`,
      );
    }
    const configText = await response.text();
    return setConfig(configText);
  } catch (error) {
    return { success: false, error: error as Error };
  }
}

export async function pushDataToSupabase(): Promise<Result<void>> {
  const state = useScoutFernoState.getState();
  const flat = state.fieldValues.reduce(
    (acc, { code, value }) => {
      acc[code] = value;
      return acc;
    },
    {} as Record<string, any>,
  );

  const payload = {
    robot_position: flat.robot_position,
    no_show: flat.no_show,
    auto_fuel_scored: flat.auto_fuel_scored,
    auto_collection_location: flat.auto_collection_location,
    auto_addition_actions: flat.auto_addition_actions,
    auto_stuck: flat.auto_stuck,
    auto_climbed: flat.auto_climbed,
    alliance_won_auto: flat.alliance_won_auto,
    teleop_fuel_scored: flat.teleop_fuel_scored,
    field_usability: flat.field_usability,
    defended_by_opponent: flat.defended_by_opponent,
    fuel_fed_passed: flat.fuel_fed_passed,
    opp_zone_actions: flat.opp_zone_actions,
    climbed: flat.climbed,
    climb_position: flat.climb_position,
    mechanical_issue: flat.mechanical_issue,
    died: flat.died,
    fell_over: flat.fell_over,
    scoring_efficiency: flat.scoring_efficiency,
    scored_how: flat.scored_how,
    scoring_location: flat.scoring_location,
    feeding_skills: flat.feeding_skills,
    passed_how: flat.passed_how,
    defense_skill: flat.defense_skill,
    cards: flat.cards,
    comments: flat.comments,
    team_number: flat.robot?.team_number,
    match_number: flat.match_number,
    competition: flat.competition,
  };

  try {
    const { error } = await supabase.from("match").insert(payload);

    if (error) {
      return { success: false, error: new Error(error.message) };
    }

    return { success: true, data: undefined };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}

export function updateValue(code: string, data: any) {
  useScoutFernoState.setState(
    produce((state: ScoutFernoState) => {
      const field = state.fieldValues.find((f) => f.code === code);
      if (field) {
        field.value = data;
      }
    }),
  );
}

export function getFieldValue(code: string) {
  return useScoutFernoState.getState().fieldValues.find((f) => f.code === code)
    ?.value;
}

export function resetFields() {
  window.dispatchEvent(new CustomEvent("resetFields", { detail: "reset" }));
}

export function forceResetFields() {
  window.dispatchEvent(
    new CustomEvent("forceResetFields", { detail: "forceReset" }),
  );
}

export function setFormData(config: Config) {
  const oldState = useScoutFernoState.getState();
  forceResetFields();
  const newFieldValues = generateFieldValues(config);
  useScoutFernoState.setState({
    ...oldState,
    fieldValues: newFieldValues,
    formData: config,
  });
}

export function setConfig(configText: string): Result<void> {
  let jsonData: any;
  try {
    jsonData = JSON.parse(configText);
  } catch (e: any) {
    return { success: false, error: e.message };
  }
  const c = configSchema.safeParse(jsonData);
  if (!c.success) {
    console.error(c.error);
    return { success: false, error: c.error };
  }
  setFormData(c.data);
  return { success: true, data: undefined };
}

export function inputSelector<T extends InputBase>(
  section: string,
  code: string,
): (state: ScoutFernoState) => T | undefined {
  return (state: ScoutFernoState) => {
    const formData = state.formData;
    const field = formData.sections
      .find((s) => s.name === section)
      ?.fields.find((f) => f.code === code);

    if (!field) {
      return undefined;
    }
    return field as T;
  };
}

export function setMatchData(matchData: MatchData[]) {
  useScoutFernoState.setState({ matchData });
}
