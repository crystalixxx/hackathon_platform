package models

import "time"

type TeamActionStatus struct {
	tableName   struct{}   `pg:"team_action_status"`
	TrackTeamID int        `pg:"track_team_id,pk"`
	TrackTeam   *TrackTeam `pg:"rel:has-one"`

	TimelineID int       `pg:"timeline_id,pk"`
	Timeline   *Timeline `pg:"rel:has-one"`

	ResultValue    int       `pg:"result_value"`
	ResolutionLink string    `pg:"resolution_link"`
	CompletedAt    time.Time `pg:"competed_at"`
	Notes          string    `pg:"notes"`
}
