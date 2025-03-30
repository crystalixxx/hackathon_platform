package models

type TrackWinner struct {
	tableName struct{} `pg:"track_winner"`
	TrackID   int      `pg:"track_id,pk"`
	Track     *Track   `pg:"rel:has-one"`

	TrackTeamID int        `pg:"track_team_id,pk"`
	TrackTeam   *TrackTeam `pg:"rel:has-one"`

	Place     int  `pg:"place"`
	IsAwardee bool `pg:"is_awardee,notnull"`
}
