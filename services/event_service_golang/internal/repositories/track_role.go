package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
)

type TrackRoleRepository struct {
	DB *pg.DB
}

func NewTrackRoleRepository(db *pg.DB) *TrackRoleRepository {
	return &TrackRoleRepository{DB: db}
}

func (r *TrackRoleRepository) Create(tx *pg.Tx, trackRole *models.TrackRole) error {
	_, err := tx.Model(trackRole).Insert()
	return err
}

func (r *TrackTeamRepository) GetUsersByTrackID(tx *pg.Tx, trackID int) ([]models.TrackTeam, error) {
	var trackTeams []models.TrackTeam
	err := tx.Model(&trackTeams).Where("track_id = ?", trackID).Select()
	return trackTeams, err
}

func (r *TrackTeamRepository) GetEventsByTeamID(tx *pg.Tx, teamID int) ([]models.TrackTeam, error) {
	var trackTeams []models.TrackTeam
	err := tx.Model(&trackTeams).Where("team_id = ?", teamID).Select()
	return trackTeams, err
}

func (r *TrackTeamRepository) GetRoleByTrackIDAndTeamID(tx *pg.Tx, trackID, teamID int) (*models.TrackTeam, error) {
	trackTeam := new(models.TrackTeam)
	err := tx.Model(trackTeam).Where("track_id = ?", trackID).Where("team_id = ?", teamID).Select()
	return trackTeam, err
}

func (r *TrackTeamRepository) SetCanViewResults(tx *pg.Tx, trackID, teamID int, canViewResults bool) error {
	_, err := tx.Model(&models.TrackTeam{}).Set("can_view_results = ?", canViewResults).Where("track_id = ?", trackID).Where("team_id = ?", teamID).Update()
	return err
}

func (r *TrackTeamRepository) SetCanViewStatistics(tx *pg.Tx, trackID, teamID int, canViewStatistics bool) error {
	_, err := tx.Model(&models.TrackTeam{}).Set("can_view_statistics = ?", canViewStatistics).Where("track_id = ?", trackID).Where("team_id = ?", teamID).Update()
	return err
}

func (r *TrackTeamRepository) DeleteTrackRole(tx *pg.Tx, trackID, teamID int) error {
	_, err := tx.Model(&models.TrackTeam{}).Where("track_id = ?", trackID).Where("team_id = ?", teamID).Delete()
	return err
}
