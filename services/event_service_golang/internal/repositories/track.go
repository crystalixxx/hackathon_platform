package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
	"time"
)

type TrackRepository struct {
	DB *pg.DB
}

func NewTrackRepository(db *pg.DB) *TrackRepository {
	return &TrackRepository{DB: db}
}

func (r *TrackRepository) Create(tx *pg.Tx, track *models.Track) error {
	_, err := tx.Model(track).Insert()
	return err
}

func (r *TrackRepository) GetAllTracks(tx *pg.Tx) ([]*models.Track, error) {
	tracks := make([]*models.Track, 0)
	err := tx.Model(&tracks).Select()
	return tracks, err
}

func (r *TrackRepository) GetAllTracksByEventID(tx *pg.Tx, eventID int) ([]*models.Track, error) {
	tracks := make([]*models.Track, 0)
	err := tx.Model(&tracks).Where("event_id = ?", eventID).Select()
	return tracks, err
}

func (r *TrackRepository) GetTracksInDateRange(tx *pg.Tx, startDate time.Time, endDate time.Time) ([]*models.Track, error) {
	tracks := make([]*models.Track, 0)
	err := tx.Model(&tracks).Relation("Date").Where("date.start_date >= ? AND date.end_date <= ?", startDate, endDate).Select()
	return tracks, err
}

func (r *TrackRepository) GetTrackByID(tx *pg.Tx, trackID int) (*models.Track, error) {
	track := new(models.Track)
	err := tx.Model(track).Where("id = ?", trackID).Select()
	return track, err
}

func (r *TrackRepository) GetTracksWithAllRelations(tx *pg.Tx) ([]*models.Track, error) {
	tracks := make([]*models.Track, 0)
	err := tx.Model(&tracks).Relation("Event").Relation("Date").Relation("TrackTeams").Relation("Participants").Relation("Timelines").Relation("TrackJudges").Relation("TrackWinners").Relation("Statuses").Select()
	return tracks, err
}

func (r *TrackRepository) UpdateTrackTitle(tx *pg.Tx, trackID int, title string) (*models.Track, error) {
	track := new(models.Track)
	_, err := tx.Model(track).Set("title = ?", title).Where("id = ?", trackID).Update()
	return track, err
}

func (r *TrackRepository) UpdateTrackDescription(tx *pg.Tx, trackID int, description string) (*models.Track, error) {
	track := new(models.Track)
	_, err := tx.Model(track).Set("description = ?", description).Where("id = ?", trackID).Update()
	return track, err
}

func (r *TrackRepository) UpdateEventID(tx *pg.Tx, trackID int, eventID int) (*models.Track, error) {
	track := new(models.Track)
	_, err := tx.Model(track).Set("event_id = ?", eventID).Where("id = ?", trackID).Update()
	return track, err
}

func (r *TrackRepository) UpdateIsScoreBased(tx *pg.Tx, trackID int, isScoreBased bool) (*models.Track, error) {
	track := new(models.Track)
	_, err := tx.Model(track).Set("is_score_based = ?", isScoreBased).Where("id = ?", trackID).Update()
	return track, err
}

func (r *TrackRepository) UpdateDateID(tx *pg.Tx, trackID int, dateID int) (*models.Track, error) {
	track := new(models.Track)
	_, err := tx.Model(track).Set("date_id = ?", dateID).Where("id = ?", trackID).Update()
	return track, err
}

func (r *TrackRepository) DeleteTrack(tx *pg.Tx, trackID int) error {
	track := new(models.Track)
	_, err := tx.Model(track).Where("id = ?", trackID).Delete()
	return err
}
