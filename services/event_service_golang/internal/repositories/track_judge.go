package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
)

type TrackJudgeRepository struct {
	DB *pg.DB
}

func NewTrackJudgeRepository(db *pg.DB) *TrackJudgeRepository {
	return &TrackJudgeRepository{DB: db}
}

func (r *TrackJudgeRepository) Create(trackJudge *models.TrackJudge) error {
	_, err := r.DB.Model(trackJudge).Insert()
	return err
}

func (r *TrackJudgeRepository) GetAllTrackJudges(TrackId int) ([]*models.TrackJudge, error) {
	trackJudges := make([]*models.TrackJudge, 0)
	err := r.DB.Model(&trackJudges).Where("track_id = ?", TrackId).Select()
	return trackJudges, err
}

func (r *TrackJudgeRepository) GetAllJudgesTracks(JudgeID int) ([]*models.TrackJudge, error) {
	trackJudges := make([]*models.TrackJudge, 0)
	err := r.DB.Model(&trackJudges).Where("judge_id = ?", JudgeID).Select()
	return trackJudges, err
}

func (r *TrackJudgeRepository) DeleteTrackJudge(TrackId int, JudgeID int) error {
	trackJudge := &models.TrackJudge{TrackID: TrackId, JudgeID: JudgeID}
	_, err := r.DB.Model(trackJudge).WherePK().Delete()
	return err
}
