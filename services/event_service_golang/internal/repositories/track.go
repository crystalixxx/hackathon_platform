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

func (r *TrackRepository) Create(track *models.Track) error {
	_, err := r.DB.Model(track).Insert()
	return err
}

func (r *TrackRepository) GetAllTracks() ([]*models.Track, error) {
	tracks := make([]*models.Track, 0)
	err := r.DB.Model(&tracks).Select()
	return tracks, err
}

func (r *TrackRepository) GetAllTracksByEventID(eventID int) ([]*models.Track, error) {
	tracks := make([]*models.Track, 0)
	err := r.DB.Model(&tracks).Where("event_id = ?", eventID).Select()
	return tracks, err
}

func (r *TrackRepository) GetTracksInDateRange(startDate time.Time, endDate time.Time) ([]*models.Track, error) {
	tracks := make([]*models.Track, 0)
	err := r.DB.Model(&tracks).Relation("Date").Where("date.start_date >= ? AND date.end_date <= ?", startDate, endDate).Select()
	return tracks, err
}

func (r *TrackRepository) GetTrackByID(trackID int) (*models.Track, error) {
	track := new(models.Track)
	err := r.DB.Model(track).Where("id = ?", trackID).Select()
	return track, err
}

func (r *TrackRepository) GetTracksWithAllRelations() ([]*models.Track, error) {
	tracks := make([]*models.Track, 0)
	err := r.DB.Model(&tracks).Relation("Event").Relation("Date").Relation("TrackTeams").Relation("Participants").Relation("Timelines").Relation("TrackJudges").Relation("TrackWinners").Relation("Statuses").Select()
	return tracks, err
}

func (r *TrackRepository) UpdateTrackTitle(trackID int, title string) (*models.Track, error) {
	track := new(models.Track)
	_, err := r.DB.Model(track).Set("title = ?", title).Where("id = ?", trackID).Update()
	return track, err
}

func (r *TrackRepository) UpdateTrackDescription(trackID int, description string) (*models.Track, error) {
	track := new(models.Track)
	_, err := r.DB.Model(track).Set("description = ?", description).Where("id = ?", trackID).Update()
	return track, err
}

func (r *TrackRepository) UpdateEventID(trackID int, eventID int) (*models.Track, error) {
	track := new(models.Track)
	_, err := r.DB.Model(track).Set("event_id = ?", eventID).Where("id = ?", trackID).Update()
	return track, err
}

func (r *TrackRepository) UpdateIsScoreBased(trackID int, isScoreBased bool) (*models.Track, error) {
	track := new(models.Track)
	_, err := r.DB.Model(track).Set("is_score_based = ?", isScoreBased).Where("id = ?", trackID).Update()
	return track, err
}

func (r *TrackRepository) UpdateDateID(trackID int, dateID int) (*models.Track, error) {
	track := new(models.Track)
	_, err := r.DB.Model(track).Set("date_id = ?", dateID).Where("id = ?", trackID).Update()
	return track, err
}

func (r *TrackRepository) DeleteTrack(trackID int) error {
	track := new(models.Track)
	_, err := r.DB.Model(track).Where("id = ?", trackID).Delete()
	return err
}
