package service

import (
	"event_service/internal/models"
	"event_service/internal/repositories"
	"event_service/internal/schemas"
	"github.com/go-pg/pg/v10"
)

type EventService struct {
	repo *repositories.EventRepository
	db   *pg.DB
}

func NewEventsService(repo *repositories.EventRepository, db *pg.DB) *EventService {
	return &EventService{
		repo: repo,
		db:   db,
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
