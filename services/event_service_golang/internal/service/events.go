package service

import (
	"event_service/internal/models"
	"event_service/internal/repositories"
	"event_service/internal/schemas"
	"github.com/go-pg/pg/v10"
	"time"
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
			tx.Rollback()
			return
		}

		err = tx.Commit()
	}()

	return s.repo.GetAllEvents(tx)
}

func (s *EventService) GetEventByID(id int) (_ *models.Event, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}
	defer func() {
		if err != nil {
			tx.Rollback()
			return
		}

		err = tx.Commit()
	}()

	return s.repo.GetEventByID(tx, id)
}

func (s *EventService) CreateEvent(event schemas.Event) (_ *models.Event, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}

	defer func() {
		if err != nil {
			tx.Rollback()
			return
		}

		tx.Commit()
	}()

	timeStart, _ := time.Parse(event.CreatedAt, time.RFC3339)
	timeEnd, _ := time.Parse(event.UpdatedAt, time.RFC3339)

	model := &models.Event{
		Title:        event.Title,
		Description:  event.Description,
		RedirectLink: event.RedirectLink,
		CreatedAt:    timeStart,
		UpdatedAt:    timeEnd,
		DateID:       event.DateId,
	}

	return s.repo.Create(tx, model)
}

func (s *EventService) UpdateEventTitle(id int, title string) (_ *models.Event, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}

	defer func() {
		if err != nil {
			tx.Rollback()
			return
		}

		tx.Commit()
	}()

	return s.repo.UpdateEventTitle(tx, id, title)
}

func (s *EventService) UpdateEventDescription(eventID int, description string) (_ *models.Event, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}
	defer func() {
		if err != nil {
			tx.Rollback()
			return
		}

		tx.Commit()
	}()

	return s.repo.UpdateEventDescription(tx, eventID, description)
}

func (s *EventService) UpdateRedirectLink(eventID int, redirectLink string) (_ *models.Event, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}
	defer func() {
		if err != nil {
			tx.Rollback()
			return
		}

		tx.Commit()
	}()

	return s.repo.UpdateRedirectLink(tx, eventID, redirectLink)
}

func (s *EventService) UpdateDateID(eventID int, dateID int) (_ *models.Event, err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return nil, err
	}
	defer func() {
		if err != nil {
			tx.Rollback()
			return
		}

		tx.Commit()
	}()

	return s.repo.UpdateDateID(tx, eventID, dateID)
}

func (s *EventService) StartEvent(eventID int) (_ *models.Event, err error) {
	// TODO: implement this method
	return nil, nil
}

func (s *EventService) EndEvent(eventID int) (_ *models.Event, err error) {
	// TODO: implement this method
	return nil, nil
}
