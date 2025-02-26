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

func (r *TrackWinnerRepository) Create(tx *pg.Tx, trackWinner *models.TrackWinner) error {
	_, err := tx.Model(trackWinner).Insert()
	return err
}

func (r *TrackWinnerRepository) GetAllTrackWinners(tx *pg.Tx) ([]*models.TrackWinner, error) {
	trackWinners := make([]*models.TrackWinner, 0)
	err := tx.Model(&trackWinners).Select()
	return trackWinners, err
}

func (r *TrackWinnerRepository) GetAllWinnersByTrackID(tx *pg.Tx, trackID int) ([]*models.TrackWinner, error) {
	trackWinners := make([]*models.TrackWinner, 0)
	err := tx.Model(&trackWinners).Where("track_id = ?", trackID).Select()
	return trackWinners, err
}

func (r *TrackWinnerRepository) GetAllTracksByTeamID(tx *pg.Tx, teamID int) ([]*models.TrackWinner, error) {
	trackWinners := make([]*models.TrackWinner, 0)
	err := tx.Model(&trackWinners).Where("track_team_id = ?", teamID).Select()
	return trackWinners, err
}

func (r *TrackWinnerRepository) GetTrackWinnerByTrackIDAndTeamID(tx *pg.Tx, trackID, teamID int) (*models.TrackWinner, error) {
	trackWinner := new(models.TrackWinner)
	err := tx.Model(trackWinner).Where("track_id = ?", trackID).Where("track_team_id = ?", teamID).Select()
	return trackWinner, err
}

func (r *TrackWinnerRepository) UpdateTrackWinnerPlace(tx *pg.Tx, trackID, teamID, place int) (*models.TrackWinner, error) {
	trackWinner := new(models.TrackWinner)
	_, err := tx.Model(trackWinner).Set("place = ?", place).Where("track_id = ?", trackID).Where("track_team_id = ?", teamID).Update()
	return trackWinner, err
}

func (r *TrackWinnerRepository) UpdateTrackWinnerAwardee(tx *pg.Tx, trackID, teamID int, isAwardee bool) (*models.TrackWinner, error) {
	trackWinner := new(models.TrackWinner)
	_, err := tx.Model(trackWinner).Set("is_awardee = ?", isAwardee).Where("track_id = ?", trackID).Where("track_team_id = ?", teamID).Update()
	return trackWinner, err
}

func (r *TrackWinnerRepository) DeleteTrackWinner(tx *pg.Tx, trackID, teamID int) error {
	trackWinner := new(models.TrackWinner)
	_, err := tx.Model(trackWinner).Where("track_id = ?", trackID).Where("track_team_id = ?", teamID).Delete()
	return err
}
