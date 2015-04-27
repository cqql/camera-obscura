package de.cqql.camera_obscura.android;

import android.app.Activity;
import android.graphics.ImageFormat;
import android.hardware.Camera;
import android.os.Bundle;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.WindowManager;

import java.io.IOException;

public class RecordingActivity extends Activity {
    private Camera camera;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.main);

        WindowManager.LayoutParams params = getWindow().getAttributes();

        // Dim the screen, to keep the camera obscura dark on the inside
        params.screenBrightness = 0;

        // But always keep it on to continue sending images. I couldn't get wake locks to work.
        params.flags |= WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON;

        getWindow().setAttributes(params);
    }

    @Override
    protected void onResume() {
        super.onResume();

        setupCamera();
    }

    @Override
    protected void onPause() {
        super.onPause();

        if (camera != null) {
            camera.stopPreview();
            camera.release();
            camera = null;
        }
    }

    private void setupCamera() {
        camera = Camera.open();

        // Rotate preview display. This value may only work on my phone.
        camera.setDisplayOrientation(90);

        Camera.Parameters params = camera.getParameters();
        params.setPictureFormat(ImageFormat.JPEG);

        // Maximum exposure time
        params.setExposureCompensation(params.getMaxExposureCompensation());

        camera.setParameters(params);

        SurfaceHolder holder = ((SurfaceView) findViewById(R.id.preview)).getHolder();

        holder.addCallback(new SurfaceHolder.Callback() {
            @Override
            public void surfaceCreated(SurfaceHolder holder) {
                try {
                    camera.setPreviewDisplay(holder);
                } catch (IOException e) {
                    e.printStackTrace();
                }

                takePicture();
            }

            @Override
            public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {

            }

            @Override
            public void surfaceDestroyed(SurfaceHolder holder) {

            }
        });
    }

    public void takePicture() {
        if (camera != null) {
            camera.startPreview();

            camera.takePicture(null, null, new Camera.PictureCallback() {
                @Override
                public void onPictureTaken(byte[] data, Camera camera) {
                    transferPicture(data, "image/jpeg");
                }
            });
        }
    }

    private void transferPicture(byte[] data, String type) {
        new UploadTask(this, type, data).execute();
    }
}
