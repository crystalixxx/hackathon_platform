package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
	"time"
)

type TimelineRepository struct {
	DB *pg.DB
}

func NewTimelineRepository(db *pg.DB) *TimelineRepository {
	return &TimelineRepository{DB: db}
}

func (r *TimelineRepository) Create(tx *pg.Tx, timeline *models.Timeline) error {
	_, err := tx.Model(timeline).Insert()
	return err
}

func (r *TimelineRepository) GetAllTimelines(tx *pg.Tx) ([]*models.Timeline, error) {
	timelines := make([]*models.Timeline, 0)
	err := tx.Model(&timelines).Select()
	return timelines, err
}

func (r *TimelineRepository) GetTimelinesWithStatus(tx *pg.Tx) ([]*models.Timeline, error) {
	timelines := make([]*models.Timeline, 0)
	err := tx.Model(&timelines).Relation("TimelineStatus").Select()
	return timelines, err
}

func (r *TimelineRepository) GetTimelinesByTrackID(tx *pg.Tx, trackID int) ([]*models.Timeline, error) {
	timelines := make([]*models.Timeline, 0)
	err := tx.Model(&timelines).Where("track_id = ?", trackID).Select()
	return timelines, err
}

func (r *TimelineRepository) GetTimelinesByTrackIDWithStatus(tx *pg.Tx, trackID int) ([]*models.Timeline, error) {
	timelines := make([]*models.Timeline, 0)
	err := tx.Model(&timelines).Where("track_id = ?", trackID).Relation("TimelineStatus").Select()
	return timelines, err
}

func (r *TimelineRepository) GetTimelineByID(tx *pg.Tx, timelineID int) (*models.Timeline, error) {
	timeline := new(models.Timeline)
	err := tx.Model(timeline).Where("id = ?", timelineID).Select()
	return timeline, err
}

func (r *TimelineRepository) UpdateTimelineTitle(tx *pg.Tx, timelineID int, title string) (*models.Timeline, error) {
	timeline := new(models.Timeline)
	_, err := tx.Model(timeline).Set("title = ?", title).Where("id = ?", timelineID).Update()
	return timeline, err
}

func (r *TimelineRepository) UpdateTimelineDescription(tx *pg.Tx, timelineID int, description string) (*models.Timeline, error) {
	timeline := new(models.Timeline)
	_, err := tx.Model(timeline).Set("description = ?", description).Where("id = ?", timelineID).Update()
	return timeline, err
}

func (r *TimelineRepository) UpdateTimelineDeadline(tx *pg.Tx, timelineID int, deadline time.Time) (*models.Timeline, error) {
	timeline := new(models.Timeline)
	_, err := tx.Model(timeline).Set("deadline = ?", deadline).Where("id = ?", timelineID).Update()
	return timeline, err
}

func (r *TimelineRepository) UpdateIsBlocking(tx *pg.Tx, timelineID int, isBlocking bool) (*models.Timeline, error) {
	timeline := new(models.Timeline)
	_, err := tx.Model(timeline).Set("is_blocking = ?", isBlocking).Where("id = ?", timelineID).Update()
	return timeline, err
}

func (r *TimelineRepository) UpdateTimelineStatus(tx *pg.Tx, timelineID, timelineStatusID int) (*models.Timeline, error) {
	timeline := new(models.Timeline)
	_, err := tx.Model(timeline).Set("timeline_status_id = ?", timelineStatusID).Where("id = ?", timelineID).Update()
	return timeline, err
}

func (r *TimelineRepository) DeleteTimeline(tx *pg.Tx, timelineID int) error {
	_, err := tx.Model(&models.Timeline{}).Where("id = ?", timelineID).Delete()
	return err
}
