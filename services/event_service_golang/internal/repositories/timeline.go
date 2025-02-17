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

func (r *TimelineRepository) Create(timeline *models.Timeline) error {
	_, err := r.DB.Model(timeline).Insert()
	return err
}

func (r *TimelineRepository) GetAllTimelines() ([]*models.Timeline, error) {
	timelines := make([]*models.Timeline, 0)
	err := r.DB.Model(&timelines).Select()
	return timelines, err
}

func (r *TimelineRepository) GetTimelinesWithStatus() ([]*models.Timeline, error) {
	timelines := make([]*models.Timeline, 0)
	err := r.DB.Model(&timelines).Relation("TimelineStatus").Select()
	return timelines, err
}

func (r *TimelineRepository) GetTimelinesByTrackID(trackID int) ([]*models.Timeline, error) {
	timelines := make([]*models.Timeline, 0)
	err := r.DB.Model(&timelines).Where("track_id = ?", trackID).Select()
	return timelines, err
}

func (r *TimelineRepository) GetTimelinesByTrackIDWithStatus(trackID int) ([]*models.Timeline, error) {
	timelines := make([]*models.Timeline, 0)
	err := r.DB.Model(&timelines).Where("track_id = ?", trackID).Relation("TimelineStatus").Select()
	return timelines, err
}

func (r *TimelineRepository) GetTimelineByID(timelineID int) (*models.Timeline, error) {
	timeline := new(models.Timeline)
	err := r.DB.Model(timeline).Where("id = ?", timelineID).Select()
	return timeline, err
}

func (r *TimelineRepository) UpdateTimelineTitle(timelineID int, title string) (*models.Timeline, error) {
	timeline := new(models.Timeline)
	_, err := r.DB.Model(timeline).Set("title = ?", title).Where("id = ?", timelineID).Update()
	return timeline, err
}

func (r *TimelineRepository) UpdateTimelineDescription(timelineID int, description string) (*models.Timeline, error) {
	timeline := new(models.Timeline)
	_, err := r.DB.Model(timeline).Set("description = ?", description).Where("id = ?", timelineID).Update()
	return timeline, err
}

func (r *TimelineRepository) UpdateTimelineDeadline(timelineID int, deadline time.Time) (*models.Timeline, error) {
	timeline := new(models.Timeline)
	_, err := r.DB.Model(timeline).Set("deadline = ?", deadline).Where("id = ?", timelineID).Update()
	return timeline, err
}

func (r *TimelineRepository) UpdateIsBlocking(timelineID int, isBlocking bool) (*models.Timeline, error) {
	timeline := new(models.Timeline)
	_, err := r.DB.Model(timeline).Set("is_blocking = ?", isBlocking).Where("id = ?", timelineID).Update()
	return timeline, err
}

func (r *TimelineRepository) UpdateTimelineStatus(timelineID, timelineStatusID int) (*models.Timeline, error) {
	timeline := new(models.Timeline)
	_, err := r.DB.Model(timeline).Set("timeline_status_id = ?", timelineStatusID).Where("id = ?", timelineID).Update()
	return timeline, err
}

func (r *TimelineRepository) DeleteTimeline(timelineID int) error {
	_, err := r.DB.Model(&models.Timeline{}).Where("id = ?", timelineID).Delete()
	return err
}
