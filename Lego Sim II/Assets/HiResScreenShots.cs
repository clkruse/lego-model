using UnityEngine;
using System.Collections;

public class HiResScreenShots : MonoBehaviour
{
	public bool processing = false;

	public int resWidth = 2550;
	public int resHeight = 3300;

	private bool takeHiResShot = false;

	public static string path;
	private static string namePrefix = "Unknown";
	public static string ScreenShotName(int width, int height)
	{
		return string.Format("/Users/ckruse/Documents/Unity/Lego Sim II/screenshots/{1} ({2}).png",
			//Application.dataPath,
			path,
			namePrefix, 
			System.DateTime.Now.ToString("yyyy-MM-dd_HH-mm-ss") + Random.Range(0, 10000));
	}

	public void TakeHiResShot(string namePrefix)
	{
		HiResScreenShots.namePrefix = namePrefix;
		processing = true;
		takeHiResShot = true;
	}

	void LateUpdate()
	{
		takeHiResShot |= Input.GetKeyDown("k");
		if (takeHiResShot)
		{
			RenderTexture rt = new RenderTexture(resWidth, resHeight, 24);
			GetComponent<Camera>().targetTexture = rt;
			Texture2D screenShot = new Texture2D(resWidth, resHeight, TextureFormat.RGB24, false);
			GetComponent<Camera>().Render();
			RenderTexture.active = rt;
			screenShot.ReadPixels(new Rect(0, 0, resWidth, resHeight), 0, 0);
			GetComponent<Camera>().targetTexture = null;
			RenderTexture.active = null; // JC: added to avoid errors
			Destroy(rt);
			byte[] bytes = screenShot.EncodeToPNG();
			string filename = ScreenShotName(resWidth, resHeight);
			System.IO.File.WriteAllBytes(filename, bytes);
			Debug.Log(string.Format("Took screenshot to: {0}", filename));
			takeHiResShot = false;
			processing = false;
		}
	}
}
