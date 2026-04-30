package com.madad

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.launch

@Composable
fun MadadApp(
    onSign: suspend () -> String,
    onText: suspend (String, String) -> String,
    onInit: () -> Unit,
    requestPerms: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    var mode by remember { mutableStateOf("sign") }
    var output by remember { mutableStateOf("") }
    var busy by remember { mutableStateOf(false) }
    var text by remember { mutableStateOf("") }

    LaunchedEffect(Unit) {
        requestPerms()
        onInit()
    }

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("Madad مدد", fontWeight = FontWeight.Bold) },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = Color(0xFF0B0F1A),
                    titleContentColor = Color(0xFFF5B700),
                ),
            )
        },
    ) { pad ->
        Column(
            Modifier.fillMaxSize().padding(pad).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            SegmentedControl(mode) { mode = it }

            when (mode) {
                "sign" -> Button(
                    enabled = !busy,
                    onClick = {
                        busy = true
                        scope.launch {
                            output = onSign()
                            busy = false
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                ) { Text(if (busy) "Translating…" else "Sign for 4 seconds", fontSize = 18.sp) }

                "voice" -> Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        text,
                        { text = it },
                        label = { Text("Speak or type") },
                        modifier = Modifier.fillMaxWidth(),
                    )
                    Button(
                        onClick = {
                            busy = true
                            scope.launch {
                                output = onText(text, "ur")
                                busy = false
                            }
                        },
                        enabled = text.isNotBlank() && !busy,
                        modifier = Modifier.fillMaxWidth(),
                    ) { Text(if (busy) "Signing…" else "Translate to PSL") }
                }
            }

            if (output.isNotBlank()) {
                Card(Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(16.dp)) { Text(output) }
                }
            }
        }
    }
}

@Composable
private fun SegmentedControl(current: String, onChange: (String) -> Unit) {
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        listOf("sign" to "Sign → Speech", "voice" to "Voice → Sign").forEach { (k, label) ->
            FilterChip(
                selected = current == k,
                onClick = { onChange(k) },
                label = { Text(label) },
            )
        }
    }
}
