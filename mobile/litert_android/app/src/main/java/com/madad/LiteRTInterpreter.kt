package com.madad

import android.content.Context
import android.graphics.Bitmap
import com.google.mediapipe.tasks.genai.llminference.GraphOptions
import com.google.mediapipe.tasks.genai.llminference.LlmInference
import com.google.mediapipe.tasks.genai.llminference.LlmInferenceSession
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlin.system.measureTimeMillis

/**
 * Thin wrapper around MediaPipe / LiteRT's on-device Gemma-4 graph.
 *
 * We initialise once at app-launch (cold start ~4 s) and reuse the session
 * across translation calls. The model file lives at
 * `assets/madad.tflite` — fetched via `make fetch-model` or a GitHub Release
 * download on first run because it is ~1.9 GB (int4).
 */
class LiteRTInterpreter(private val ctx: Context) {

    private lateinit var engine: LlmInference
    private lateinit var session: LlmInferenceSession

    suspend fun initialise() = withContext(Dispatchers.IO) {
        val modelPath = FileExtractor.ensureAsset(ctx, "madad.tflite")
        val opts = LlmInference.LlmInferenceOptions.builder()
            .setModelPath(modelPath)
            .setMaxTokens(512)
            .setMaxTopK(1)  // greedy; matches backend temperature 0.1
            .setPreferredBackend(LlmInference.Backend.GPU)
            .build()
        engine = LlmInference.createFromOptions(ctx, opts)

        val sessionOpts = LlmInferenceSession.LlmInferenceSessionOptions.builder()
            .setTopK(1)
            .setTemperature(0.1f)
            .setGraphOptions(
                GraphOptions.builder()
                    .setEnableVisionModality(true)
                    .setEnableAudioModality(true)
                    .build()
            )
            .build()
        session = LlmInferenceSession.createFromOptions(engine, sessionOpts)
    }

    /** Sign → JSON (Urdu + English + glosses). Blocks for ~1-3 s. */
    suspend fun signToText(frames: List<Bitmap>, langHint: String): String = withContext(Dispatchers.Default) {
        session.addQueryChunk(PromptBuilder.system())
        session.addQueryChunk(PromptBuilder.userSignToText(langHint))
        frames.forEach { session.addImage(it) }
        val out: String
        val ms = measureTimeMillis { out = session.generateResponse() }
        android.util.Log.i("Madad", "sign-to-text ${ms}ms")
        session.resetSession()
        out
    }

    suspend fun textToSign(text: String, sourceLang: String, vocab: List<String>): String =
        withContext(Dispatchers.Default) {
            session.addQueryChunk(PromptBuilder.systemTextToSign())
            session.addQueryChunk(PromptBuilder.userTextToSign(text, sourceLang, vocab))
            val out = session.generateResponse()
            session.resetSession()
            out
        }

    fun close() {
        session.close()
        engine.close()
    }
}
