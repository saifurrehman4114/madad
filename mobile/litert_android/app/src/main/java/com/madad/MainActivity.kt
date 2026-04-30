package com.madad

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {

    private lateinit var engine: LiteRTInterpreter
    private lateinit var recorder: CameraRecorder

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { /* handled via state */ }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        engine = LiteRTInterpreter(this)
        recorder = CameraRecorder(this)

        setContent {
            MaterialTheme {
                MadadApp(
                    onSign = ::translateSignToText,
                    onText = ::translateTextToSign,
                    onInit = ::init,
                    requestPerms = {
                        permissionLauncher.launch(
                            arrayOf(Manifest.permission.CAMERA, Manifest.permission.RECORD_AUDIO)
                        )
                    },
                )
            }
        }
    }

    private fun init() = lifecycleScope.launch {
        if (hasPermissions()) {
            engine.initialise()
            recorder.initialise()
        }
    }

    private fun hasPermissions(): Boolean =
        listOf(Manifest.permission.CAMERA, Manifest.permission.RECORD_AUDIO).all {
            ContextCompat.checkSelfPermission(this, it) == PackageManager.PERMISSION_GRANTED
        }

    private suspend fun translateSignToText(): String {
        val frames: List<Bitmap> = recorder.record(4_000)
        return engine.signToText(frames, "ur")
    }

    private suspend fun translateTextToSign(text: String, lang: String): String =
        engine.textToSign(text, lang, AvatarVocab.DEFAULT)

    override fun onDestroy() {
        engine.close()
        recorder.release()
        super.onDestroy()
    }
}
