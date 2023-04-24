package main

import (
	"fmt"
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
	"github.com/eiannone/keyboard"
	"time"
)

type WordCounterApp struct {
	wordsLabel     *widget.Label
	misshitLabel   *widget.Label
	timeLabel      *widget.Label
	scoreTable     *widget.Label
	startButton    *widget.Button
	resetButton    *widget.Button
	wordCount      int
	misshitCount   int
	timeLeft       int
	running        bool
	scores         []string
	quitKeyboardCh chan bool
}

func (app *WordCounterApp) startCountdown() {
	app.resetCounter()
	app.startButton.Disable()
	app.resetButton.Disable()
	app.timeLabel.SetText("Starting in 4 seconds...")

	go func() {
		for i := 3; i > 0; i-- {
			time.Sleep(time.Second)
			app.timeLabel.SetText(fmt.Sprintf("Starting in %d seconds...", i))
		}
		time.Sleep(time.Second)
		app.startTimer()
	}()
}

func (app *WordCounterApp) startTimer() {
	app.running = true
	app.timeLeft = 60
	app.updateLabels()

	go func() {
		for app.timeLeft > 0 {
			time.Sleep(time.Second)
			app.timeLeft--
			app.updateLabels()
		}
		app.stopTimer()
	}()
}

func (app *WordCounterApp) stopTimer() {
	app.running = false
	app.startButton.Enable()
	app.resetButton.Enable()
	app.updateLabels()
	app.updateScoreTable()
}

func (app *WordCounterApp) resetCounter() {
	app.wordCount = 0
	app.misshitCount = 0
	app.updateLabels()
}

func (app *WordCounterApp) updateLabels() {
	app.wordsLabel.SetText(fmt.Sprintf("Words per Minute: %d", app.wordCount))
	app.misshitLabel.SetText(fmt.Sprintf("Misshit Count: %d", app.misshitCount))
	app.timeLabel.SetText(fmt.Sprintf("Time Left: %d", app.timeLeft))
}

func (app *WordCounterApp) updateScoreTable() {
	app.scores = append(app.scores, fmt.Sprintf("Words: %d, Misshits: %d", app.wordCount, app.misshitCount))
	scoreTableText := "Score Table:\n"
	for idx, score := range app.scores {
		scoreTableText += fmt.Sprintf("%d. %s\n", idx+1, score)
	}
	app.scoreTable.SetText(scoreTableText)
}

func main() {
	myApp := app.New()
	myWindow := myApp.NewWindow("Word Counter")

	wordCounterApp := &WordCounterApp{
		wordsLabel:   widget.NewLabel("Words per Minute: 0"),
		misshitLabel: widget.NewLabel("Misshit Count: 0"),
		timeLabel:    widget.NewLabel("Time Left: 0"),
		scoreTable:   widget.NewLabel("Score Table:"),
	}

	wordCounterApp.startButton = widget.NewButton("Start", wordCounterApp.startCountdown)
	wordCounterApp.resetButton = widget.NewButton("Reset Counter", wordCounterApp.resetCounter)

	content := container.NewVBox(
		container.NewHBox(wordCounterApp.wordsLabel, wordCounterApp.misshitLabel, wordCounterApp.timeLabel),
		container.NewHBox(wordCounterApp.startButton, wordCounterApp.resetButton),
		wordCounterApp.scoreTable,
	)

	myWindow.SetContent(content)
	myWindow.Resize(fyne.NewSize(500, 300))

	err := keyboard.Open()
	if err != nil {
		panic(err)
	}
	defer func() {
		err := keyboard.Close()
		if err != nil {

		}
	}()

	wordCounterApp.quitKeyboardCh = make(chan bool)
	go func() {
		for {
			char, key, err := keyboard.GetKey()
			if err != nil {
				panic(err)
			}

			if wordCounterApp.running {
				if key == keyboard.KeySpace || key == keyboard.KeyEnter {
					wordCounterApp.wordCount++
					wordCounterApp.updateLabels()
				} else if key == keyboard.KeyBackspace {
					wordCounterApp.misshitCount++
					wordCounterApp.updateLabels()
				}
			}

			if char == 'q' {
				wordCounterApp.quitKeyboardCh <- true
			}
		}
	}()

	myWindow.ShowAndRun()
	<-wordCounterApp.quitKeyboardCh
}
