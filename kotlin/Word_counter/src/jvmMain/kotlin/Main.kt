import androidx.compose.material.MaterialTheme
import androidx.compose.desktop.ui.tooling.preview.Preview
import androidx.compose.material.Button
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application

fun main() = Window {
    DesktopMaterialTheme {
        WordCounterApp()
    }
}

@Composable
fun WordCounterApp() {
    var wordCount by remember { mutableStateOf(0) }
    var misshitCount by remember { mutableStateOf(0) }
    var timeLeft by remember { mutableStateOf(0) }
    var isRunning by remember { mutableStateOf(false) }

    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
    ) {
        Text(
            text = "Words per Minute: $wordCount\nMisshit Count: $misshitCount\nTime Left: $timeLeft",
            fontSize = 18.sp
        )

        Spacer(modifier = Modifier.height(16.dp))

        Row {
            Button(
                onClick = {
                    if (!isRunning) {
                        startCountdown(timeLeft, isRunning)
                    }
                },
                enabled = !isRunning
            ) {
                Text("Start")
            }

            Spacer(modifier = Modifier.width(16.dp))

            Button(onClick = { resetCounter(wordCount, misshitCount) }, enabled = !isRunning) {
                Text("Reset Counter")
            }
        }
    }
}

@Composable
fun startCountdown(timeLeft: MutableState<Int>, isRunning: MutableState<Boolean>) {
    val countdownScope = rememberCoroutineScope()
    countdownScope.launch {
        for (i in 4 downTo 1) {
            timeLeft.value = i
            delay(1000)
        }
        startTimer(timeLeft, isRunning)
    }
}

@Composable
fun startTimer(timeLeft: MutableState<Int>, isRunning: MutableState<Boolean>) {
    isRunning.value = true
    timeLeft.value = 60

    val timerScope = rememberCoroutineScope()
    timerScope.launch {
        while (timeLeft.value > 0) {
            delay(1000)
            timeLeft.value -= 1
        }
        isRunning.value = false
    }
}

@Composable
fun resetCounter(wordCount: MutableState<Int>, misshitCount: MutableState<Int>) {
    wordCount.value = 0
    misshitCount.value = 0
}
