import io
import unittest

from PIL import Image

from app import app, model_mgr


class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.client = app.test_client()

    def test_main_pages_load(self):
        for path in (
            "/",
            "/CropRecommendation.html",
            "/FertilizerRecommendation.html",
            "/PesticideRecommendation.html",
        ):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_crop_recommendation(self):
        response = self.client.post(
            "/crop_prediction",
            data={
                "nitrogen": "90",
                "phosphorous": "42",
                "potassium": "43",
                "temperature": "20.5",
                "humidity": "82",
                "ph": "6.5",
                "rainfall": "202.9",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Recommended Crop", response.data)

    def test_fertilizer_recommendation(self):
        response = self.client.post(
            "/fertilizer-predict",
            data={
                "cropname": "maize",
                "nitrogen": "80",
                "phosphorous": "40",
                "potassium": "30",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NPK Analysis Results", response.data)

    def test_pest_recommendation(self):
        image_bytes = io.BytesIO()
        Image.new("RGB", (96, 96), color=(112, 145, 73)).save(image_bytes, format="PNG")
        image_bytes.seek(0)

        model_mgr.pest_classifier = None
        response = self.client.post(
            "/predict",
            data={"image": (image_bytes, "pest.png")},
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Recommended Pesticides", response.data)

    def test_rejects_invalid_image_content(self):
        response = self.client.post(
            "/predict",
            data={"image": (io.BytesIO(b"not an image"), "fake.jpg")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"not a valid image", response.data)


if __name__ == "__main__":
    unittest.main()
