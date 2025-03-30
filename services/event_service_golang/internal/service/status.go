package service

import (
	"event_service/internal/models"
	"event_service/internal/repositories"
	"event_service/internal/schemas"
	"github.com/go-pg/pg/v10"
)

type StatusService struct {
	repo *repositories.StatusRepository
	db   *pg.DB
}

func NewStatusService(repo *repositories.StatusRepository, db *pg.DB) *StatusService {
	return &StatusService{
		repo: repo,
		db:   db,
	}
}

func (s *StatusService) GetAllStatuses() (_ []*models.Status, err error) {
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

	return s.repo.GetAllStatuses(tx)
}

func (s *StatusService) GetStatusById(statusId int) (_ *models.Status, err error) {
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

	return s.repo.GetStatusById(tx, statusId)
}

func (s *StatusService) CreateStatus(status schemas.Status) (_ *models.Status, err error) {
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

	statusModel := &models.Status{
		Title:       status.Title,
		Description: status.Description,
	}

	return s.repo.Create(tx, statusModel)
}

func (s *StatusService) UpdateStatus(eventId int, newStatus schemas.Status) (_ *models.Status, err error) {
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

	status, err := s.GetStatusById(eventId)
	if err != nil {
		return status, err
	}

	if newStatus.Title != "" {
		status.Title = newStatus.Title
	}

	if newStatus.Description != "" {
		status.Description = newStatus.Description
	}

	return s.repo.UpdateStatus(tx, status)
}

func (s *StatusService) DeleteStatus(statusId int) (err error) {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}

	defer func() {
		if err != nil {
			_ = tx.Rollback()
			return
		}

		err = tx.Commit()
	}()

	return s.repo.DeleteStatus(tx, statusId)
}
