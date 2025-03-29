package service

import (
	"event_service/internal/models"
	"event_service/internal/repositories"
	"event_service/internal/schemas"
	"github.com/go-pg/pg/v10"
)

type DateService struct {
	repo *repositories.DateRepository
	db   *pg.DB
}

func NewDateService(repo *repositories.DateRepository, db *pg.DB) *DateService {
	return &DateService{
		repo: repo,
		db:   db,
	}
}

func (s *DateService) GetAllDates() ([]*models.Date, error) {
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

	return s.repo.GetAllDates(tx)
}

func (s *DateService) GetDateByID(id int) (*models.Date, error) {
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

	return s.repo.GetDateById(tx, id)
}

func (s *DateService) CreateDate(date schemas.Date) (*models.Date, error) {
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

	model := models.Date{
		DateStart: date.DateStart,
		DateEnd:   date.DateEnd,
	}

	return s.repo.Create(tx, &model)
}

func (s *DateService) UpdateDate(id int, date schemas.Date) (*models.Date, error) {
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

	_, err = s.repo.ChangeDateStart(tx, id, date.DateStart)
	if err != nil {
		return nil, err
	}

	model, err := s.repo.ChangeDateEnd(tx, id, date.DateEnd)
	if err != nil {
		return nil, err
	}

	return model, nil
}

func (s *DateService) DeleteDate(id int) error {
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

	return s.repo.DeleteDate(tx, id)
}
