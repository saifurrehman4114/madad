package com.madad

import android.content.Context
import android.graphics.Bitmap
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import androidx.camera.lifecycle.ProcessCameraProvider
import kotlinx.coroutines.CompletableDeferred
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.withContext
import java.util.concurrent.Executors

/**
 * CameraX wrapper that captures ``n`` frames over ``durationMs`` at a target
 * sampling rate of 4 fps (matches the backend). We deliberately do NOT use
 * the Recorder API — we want individual frames, not an encoded video file.
 */
class CameraRecorder(private val ctx: Context) {

    private val executor = Executors.newSingleThreadExecutor()
    private var analyser: ImageAnalysis? = null
    private val queue = ArrayDeque<Bitmap>(16)

    suspend fun initialise() = withContext(Dispatchers.Main) {
        val provider = ProcessCameraProvider.getInstance(ctx).get()
        analyser = ImageAnalysis.Builder()
            .setTargetResolution(android.util.Size(480, 640))
            .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
            .build()
            .apply {
                setAnalyzer(executor) { proxy: ImageProxy ->
                    queue.addLast(proxy.toBitmap())
                    while (queue.size > 16) queue.removeFirst()
                    proxy.close()
                }
            }
        provider.unbindAll()
        // lifecycleOwner binding is done from the activity in real code
    }

    suspend fun record(durationMs: Long): List<Bitmap> {
        queue.clear()
        val stride = durationMs / 16
        val frames = mutableListOf<Bitmap>()
        val deadline = System.currentTimeMillis() + durationMs
        while (System.currentTimeMillis() < deadline) {
            delay(stride)
            queue.lastOrNull()?.let { frames.add(it) }
        }
        return frames.takeLast(16)
    }

    fun release() {
        executor.shutdownNow()
    }

    private fun ImageProxy.toBitmap(): Bitmap {
        val buffer = planes[0].buffer
        val bytes = ByteArray(buffer.remaining())
        buffer.get(bytes)
        return android.graphics.BitmapFactory.decodeByteArray(bytes, 0, bytes.size)
    }
}
