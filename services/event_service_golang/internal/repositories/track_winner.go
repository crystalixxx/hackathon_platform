package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
)

type TrackWinnerRepository struct {
	DB *pg.DB
}

func NewTrackWinnerRepository(db *pg.DB) *TrackWinnerRepository {
	return &TrackWinnerRepository{DB: db}
}

func (r *TrackWinnerRepository) Create(trackWinner *models.TrackWinner) error {
	_, err := r.DB.Model(trackWinner).Insert()
	return err
}

func (r *TrackWinnerRepository) GetAllTrackWinners() ([]*models.TrackWinner, error) {
	trackWinners := make([]*models.TrackWinner, 0)
	err := r.DB.Model(&trackWinners).Select()
	return trackWinners, err
}

func (r *TrackWinnerRepository) GetAllWinnersByTrackID(trackID int) ([]*models.TrackWinner, error) {
	trackWinners := make([]*models.TrackWinner, 0)
	err := r.DB.Model(&trackWinners).Where("track_id = ?", trackID).Select()
	return trackWinners, err
}

func (r *TrackWinnerRepository) GetAllTracksByTeamID(teamID int) ([]*models.TrackWinner, error) {
	trackWinners := make([]*models.TrackWinner, 0)
	err := r.DB.Model(&trackWinners).Where("track_team_id = ?", teamID).Select()
	return trackWinners, err
}

func (r *TrackWinnerRepository) GetTrackWinnerByTrackIDAndTeamID(trackID, teamID int) (*models.TrackWinner, error) {
	trackWinner := new(models.TrackWinner)
	err := r.DB.Model(trackWinner).Where("track_id = ?", trackID).Where("track_team_id = ?", teamID).Select()
	return trackWinner, err
}

func (r *TrackWinnerRepository) UpdateTrackWinnerPlace(trackID, teamID, place int) (*models.TrackWinner, error) {
	trackWinner := new(models.TrackWinner)
	_, err := r.DB.Model(trackWinner).Set("place = ?", place).Where("track_id = ?", trackID).Where("track_team_id = ?", teamID).Update()
	return trackWinner, err
}

func (r *TrackWinnerRepository) UpdateTrackWinnerAwardee(trackID, teamID int, isAwardee bool) (*models.TrackWinner, error) {
	trackWinner := new(models.TrackWinner)
	_, err := r.DB.Model(trackWinner).Set("is_awardee = ?", isAwardee).Where("track_id = ?", trackID).Where("track_team_id = ?", teamID).Update()
	return trackWinner, err
}

func (r *TrackWinnerRepository) DeleteTrackWinner(trackID, teamID int) error {
	trackWinner := new(models.TrackWinner)
	_, err := r.DB.Model(trackWinner).Where("track_id = ?", trackID).Where("track_team_id = ?", teamID).Delete()
	return err
}
