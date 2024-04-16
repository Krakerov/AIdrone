using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO.Ports;

public class Sim2Arduino : MonoBehaviour
{
    SerialPort port = new SerialPort("COM9", 115200);
    public string data_string;
    public MoveDrone MoveDrone;
    public float maksThrust = 0.25f;
    void Start()
    {
        port.Open();
        MoveDrone = GetComponent<MoveDrone>();
        InvokeRepeating("func", 0, 0.5f);
    }

    // Update is called once per frame
    void func()
    {
        data_string = "";
        data_string += (transform.rotation.z*57).ToString().Replace(",", ".")+","; // 57 = 360/2п
        data_string += (transform.rotation.x*57).ToString().Replace(",", ".")+",";
        data_string += (MoveDrone.SumThrust*maksThrust).ToString().Replace(",", ".")+",";
        data_string += 0.ToString().Replace(",", ".")+",";
        port.Write(data_string);
        Debug.Log(data_string);
    }
}
