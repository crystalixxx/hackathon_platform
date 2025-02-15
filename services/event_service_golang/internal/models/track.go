package models

type Track struct {
	ID           int    `pg:"id,pk"`
	Title        string `pg:"title,type:varchar(255)"`
	Description  string `pg:"description"`
	IsScoreBased bool   `pg:"is_score_based"`

	EventID int    `pg:"event_id"`
	Event   *Event `pg:"rel:has-one"`

	DateID int   `pg:"date_id"`
	Date   *Date `pg:"rel:has-one"`

	TrackTeams   []TrackTeam   `pg:"rel:has-many"`
	Participants []TrackRole   `pg:"rel:has-many"`
	Timelines    []Timeline    `pg:"rel:has-many"`
	TrackJudges  []TrackJudge  `pg:"many2many:track_judges"`
	TrackWinners []TrackWinner `pg:"many2many:track_winners"`
	Statuses     []Status      `pg:"many2many:status_tracks"`
}
