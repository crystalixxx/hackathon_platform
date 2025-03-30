package service

import (
	"event_service/internal/models"
	"event_service/internal/repositories"
	"event_service/internal/schemas"
	"github.com/go-pg/pg/v10"
)

type EventService struct {
	repo              *repositories.EventRepository
	statusEventRepo   *repositories.StatusEventRepository
	locationEventRepo *repositories.EventLocationRepository
	db                *pg.DB
}

func NewEventsService(repo *repositories.EventRepository, statusEventRepo *repositories.StatusEventRepository, db *pg.DB) *EventService {
	return &EventService{
		repo:            repo,
		statusEventRepo: statusEventRepo,
		db:              db,
	}
}

func (s *EventService) GetAllEvents() (_ []*models.Event, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}
	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		err = tx.Commit()
	}()

	return s.repo.GetAllEvents(tx)
}

func (s *EventService) GetEventByID(eventId int) (_ *models.Event, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}
	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		err = tx.Commit()
	}()

	return s.repo.GetEventByID(tx, eventId)
}

func (s *EventService) GetEventByStatus(status string) (_ []*models.Event, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}
	defer func() {
		if err != nil {
			_ = tx.Rollback()
		}

		err = tx.Commit()
	}()

	return s.repo.GetEventByStatus(tx, status)
}

func (s *EventService) CreateEvent(event schemas.Event) (_ *models.Event, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		_ = tx.Commit()
	}()

	model := &models.Event{
		Title:        event.Title,
		Description:  event.Description,
		RedirectLink: event.RedirectLink,
		DateID:       event.DateId,
		Status:       event.Status,
	}

	return s.repo.Create(tx, model)
}

func (s *EventService) UpdateEvent(eventId int, newEvent schemas.EventUpdate) (_ *models.Event, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		_ = tx.Commit()
	}()

	event, err := s.GetEventByID(eventId)
	if err != nil {
		return nil, err
	}

	if newEvent.Title != "" {
		event.Title = newEvent.Title
	}

	if newEvent.Description != "" {
		event.Description = newEvent.Description
	}

	if newEvent.RedirectLink != "" {
		event.RedirectLink = newEvent.RedirectLink
	}

	if newEvent.DateId != 0 {
		event.DateID = newEvent.DateId
	}

	if newEvent.Status != "" {
		event.Status = newEvent.Status
	}

	return s.repo.UpdateEvent(tx, eventId, event)
}

func (s *EventService) DeleteEvent(eventID int) (err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		_ = tx.Commit()
	}()

	return s.repo.DeleteEvent(tx, eventID)
}

func (s *EventService) StartEvent(eventID int) (_ *models.Event, err error) {
	// TODO: implement this method
	return nil, nil
}

func (s *EventService) EndEvent(eventID int) (_ *models.Event, err error) {
	// TODO: implement this method
	return nil, nil
}

func (s *EventService) GetAllEventStatuses(eventID int) (_ []*models.Status, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		_ = tx.Commit()
	}()

	return s.statusEventRepo.GetAllEventsStatuses(tx, eventID)
}

func (s *EventService) AddStatusToEvent(statusEventSchema *schemas.StatusEvent) (_ *models.StatusEvent, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		_ = tx.Commit()
	}()

	statusEventModel := &models.StatusEvent{
		EventID:  statusEventSchema.EventID,
		StatusID: statusEventSchema.StatusID,
	}

	return s.statusEventRepo.Create(tx, statusEventModel)
}

func (s *EventService) RemoveStatusFromEvent(statusEventSchema *schemas.StatusEvent) (err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		_ = tx.Commit()
	}()

	return s.statusEventRepo.DeleteStatusEvent(tx, statusEventSchema.StatusID, statusEventSchema.EventID)
}

func (s *EventService) GetAllEventLocations(eventId int) (_ []*models.Location, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		_ = tx.Commit()
	}()

	return s.locationEventRepo.GetAllEventsLocations(tx, eventId)
}

func (s *EventService) AddLocationToEvent(locationEventSchema *schemas.EventLocation) (_ *models.EventLocation, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		_ = tx.Commit()
	}()

	locationEventModel := &models.EventLocation{
		EventID:    locationEventSchema.EventID,
		LocationID: locationEventSchema.LocationID,
	}

	return s.locationEventRepo.Create(tx, locationEventModel)
}

func (s *EventService) RemoveLocationFromEvent(statusEventSchema *schemas.EventLocation) (err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		_ = tx.Commit()
	}()

	return s.locationEventRepo.DeleteEventLocation(tx, statusEventSchema.EventID, statusEventSchema.LocationID)
}
