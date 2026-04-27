import { useEvent } from "../../hooks";
import {
  getFieldValue,
  inputSelector,
  updateValue,
  useScoutFernoState,
} from "../../store/store";
import React, { useCallback, useEffect, useMemo } from "react";
import { TBATeamAndRobotInputData } from "./BaseInputProps";
import { ConfigurableInputProps } from "./ConfigurableInput";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../components/ui/select";
import { Input } from "../../components/ui/input";

interface TBATeamAndRobotData {
  team_number: number;
  robot_position: string;
}

export default function TBATeamAndRobotInput(props: ConfigurableInputProps) {
  const data = useScoutFernoState(
    inputSelector<TBATeamAndRobotInputData>(props.section, props.code)
  );
  const matchData = useScoutFernoState((state) => state.matchData);
  const selectedMatchNumber = useScoutFernoState(() => {
    const value = getFieldValue("match_number");
    return typeof value === "number" ? value : null;
  });
  // See !108. Some teams may want to assign scouts to a specific driver station
  // (e.g. Red 1, Red 2, Red 3, Blue 1, Blue 2, Blue 3) across matches. To save time
  // and reduce errors, we can automatically select the team and robot position based
  // on the selected match number and driver station.
  //
  // By temporary convention, we assume the field for driver station selection is
  // called "driverStation" and contains values like "R1", "R2", "R3", "B1", "B2",
  // "B3". If the driver station field is present and has a valid value, we will
  // automatically select the corresponding team and robot position for the scout.
  //
  // This is an optional feature that can be used by teams who want it, and it will
  // eventually graduate into explicit config.
  const driverStation = useScoutFernoState(() => {
    return getFieldValue("driverStation");
  });

  if (!data) {
    return <div>Invalid input</div>;
  }

  const [value, setValue] = React.useState<TBATeamAndRobotData | null>(
    data.defaultValue || null
  );

  // Find all team options from the selected match
  const teamOptions = useMemo(() => {
    if (!matchData || matchData.length === 0 || !selectedMatchNumber) {
      return [];
    }

    // Filter for qualification matches only
    const match = matchData.find(
      (m) => m.comp_level === "qm" && m.match_number === selectedMatchNumber
    );

    if (!match) return [];

    // Extract all team numbers from both alliances with their positions
    const teams: Array<{
      team_number: number;
      robot_position: string;
      alliance: string;
      position: number;
    }> = [];

    // Red alliance teams
    match.alliances.red.team_keys.forEach((teamKey, index) => {
      const team_number = parseInt(teamKey.substring(3));
      if (!isNaN(team_number)) {
        teams.push({
          team_number,
          robot_position: `R${index + 1}`,
          alliance: "Red",
          position: index + 1,
        });
      }
    });

    // Blue alliance teams
    match.alliances.blue.team_keys.forEach((teamKey, index) => {
      const team_number = parseInt(teamKey.substring(3));
      if (!isNaN(team_number)) {
        teams.push({
          team_number,
          robot_position: `B${index + 1}`,
          alliance: "Blue",
          position: index + 1,
        });
      }
    });

    return teams;
  }, [matchData, selectedMatchNumber]);

  // Automatically select team and robot based on selected driver station and match number
  useEffect(() => {
    if (driverStation !== "") {
      const team_number = teamOptions.find(
        (team) => team.robot_position == driverStation
      )?.team_number;
      if (team_number !== undefined) {
        setValue({
          team_number,
          robot_position: driverStation,
        });
      }
    }
  }, [teamOptions, selectedMatchNumber, driverStation]);

  const resetState = useCallback(
    ({ force }: { force: boolean }) => {
      if (force) {
        setValue(data.defaultValue || null);
        return;
      }
      if (data.formResetBehavior === "preserve") {
        return;
      }
      setValue(data.defaultValue || null);
    },
    [data.defaultValue, data.formResetBehavior]
  );

  useEvent("resetFields", resetState);

  useEffect(() => {
    updateValue(props.code, value);
  }, [value, props.code]);

  const handleSelectChange = useCallback((selectedValue: string) => {
    const [team_number, robot_position] = selectedValue.split("|");
    setValue({
      team_number: parseInt(team_number),
      robot_position,
    });
  }, []);

  // Use a dropdown select if we have team options, otherwise use a regular number input
  if (teamOptions.length > 0) {
    return (
      <Select
        name={data.title}
        onValueChange={handleSelectChange}
        value={value ? `${value.team_number}|${value.robot_position}` : ""}
      >
        <SelectTrigger>
          <SelectValue placeholder="Select a team" />
        </SelectTrigger>
        <SelectContent>
          {teamOptions.map((team) => (
            <SelectItem
              key={`${team.team_number}|${team.robot_position}`}
              value={`${team.team_number}|${team.robot_position}`}
            >
              Team {team.team_number} ({team.alliance} {team.position})
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    );
  }

  // Fall back to standard number input if no team options are available
  return (
    <Input
      type="number"
      value={value?.team_number || ""}
      id={data.title}
      onChange={(e) => {
        const parsed = Number(e.target.value);
        if (e.target.value === "") {
          setValue(null);
          return;
        }
        if (isNaN(parsed)) {
          return;
        }
        setValue({
          team_number: parsed,
          robot_position: "",
        });
      }}
      placeholder="Enter team number"
    />
  );
}
