package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
)

type TrackTeamRepository struct {
	DB *pg.DB
}

func NewTrackTeamRepository(db *pg.DB) *TrackTeamRepository {
	return &TrackTeamRepository{DB: db}
}

func (r *TrackTeamRepository) Create(trackTeam *models.TrackTeam) error {
	_, err := r.DB.Model(trackTeam).Insert()
	return err
}

func (r *TrackTeamRepository) GetTeamsByTrackID(trackID int) ([]models.TrackTeam, error) {
	var trackTeams []models.TrackTeam
	err := r.DB.Model(&trackTeams).Where("track_id = ?", trackID).Select()
	return trackTeams, err
}

func (r *TrackTeamRepository) GetTracksByTeamID(teamID int) ([]models.TrackTeam, error) {
	var trackTeams []models.TrackTeam
	err := r.DB.Model(&trackTeams).Where("team_id = ?", teamID).Select()
	return trackTeams, err
}

func (r *TrackTeamRepository) GetByTrackIDAndTeamID(trackID, teamID int) (*models.TrackTeam, error) {
	trackTeam := new(models.TrackTeam)
	err := r.DB.Model(trackTeam).Where("track_id = ?", trackID).Where("team_id = ?", teamID).Select()
	return trackTeam, err
}

func (r *TrackTeamRepository) SetActive(trackID, teamID int, isActive bool) error {
	_, err := r.DB.Model(&models.TrackTeam{}).Set("is_active = ?", isActive).Where("track_id = ?", trackID).Where("team_id = ?", teamID).Update()
	return err
}

func (r *TrackTeamRepository) DeleteTrackTeam(trackID, teamID int) error {
	_, err := r.DB.Model(&models.TrackTeam{}).Where("track_id = ?", trackID).Where("team_id = ?", teamID).Delete()
	return err
}
