package models

type Track struct {
	tableName    struct{} `pg:"track"`
	ID           int      `pg:"id,pk"`
	Title        string   `pg:"title,type:varchar(255),notnull"`
	Description  string   `pg:"description"`
	IsScoreBased bool     `pg:"is_score_based,notnull"`

	EventID int    `pg:"event_id"`
	Event   *Event `pg:"rel:has-one"`

	DateID int   `pg:"date_id"`
	Date   *Date `pg:"rel:has-one"`

	TrackTeams   []TrackTeam   `pg:"rel:has-many"`
	Participants []TrackRole   `pg:"rel:has-many"`
	Timelines    []Timeline    `pg:"rel:has-many"`
	TrackJudges  []TrackJudge  `pg:"many2many:track_judge"`
	TrackWinners []TrackWinner `pg:"many2many:track_winner"`
	Statuses     []Status      `pg:"many2many:status_track"`
	Locations    []Location    `pg:"many2many:location_track"`
}
