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

func (r *TrackRoleRepository) Create(trackRole *models.TrackRole) error {
	_, err := r.DB.Model(trackRole).Insert()
	return err
}

func (r *TrackTeamRepository) GetUsersByTrackID(trackID int) ([]models.TrackTeam, error) {
	var trackTeams []models.TrackTeam
	err := r.DB.Model(&trackTeams).Where("track_id = ?", trackID).Select()
	return trackTeams, err
}

func (r *TrackTeamRepository) GetEventsByTeamID(teamID int) ([]models.TrackTeam, error) {
	var trackTeams []models.TrackTeam
	err := r.DB.Model(&trackTeams).Where("team_id = ?", teamID).Select()
	return trackTeams, err
}

func (r *TrackTeamRepository) GetRoleByTrackIDAndTeamID(trackID, teamID int) (*models.TrackTeam, error) {
	trackTeam := new(models.TrackTeam)
	err := r.DB.Model(trackTeam).Where("track_id = ?", trackID).Where("team_id = ?", teamID).Select()
	return trackTeam, err
}

func (r *TrackTeamRepository) SetCanViewResults(trackID, teamID int, canViewResults bool) error {
	_, err := r.DB.Model(&models.TrackTeam{}).Set("can_view_results = ?", canViewResults).Where("track_id = ?", trackID).Where("team_id = ?", teamID).Update()
	return err
}

func (r *TrackTeamRepository) SetCanViewStatistics(trackID, teamID int, canViewStatistics bool) error {
	_, err := r.DB.Model(&models.TrackTeam{}).Set("can_view_statistics = ?", canViewStatistics).Where("track_id = ?", trackID).Where("team_id = ?", teamID).Update()
	return err
}

func (r *TrackTeamRepository) DeleteTrackRole(trackID, teamID int) error {
	_, err := r.DB.Model(&models.TrackTeam{}).Where("track_id = ?", trackID).Where("team_id = ?", teamID).Delete()
	return err
}
