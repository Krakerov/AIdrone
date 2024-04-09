using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO.Ports;

public class Sim2Arduino : MonoBehaviour
{
    SerialPort port = new SerialPort("COM9", 9600);
    public string data_string;
    public MoveDrone MoveDrone;
    void Start()
    {
        port.Open();
        MoveDrone = GetComponent<MoveDrone>();
    }

    // Update is called once per frame
    void Update()
    {
        data_string = "";
        data_string += transform.rotation.z.ToString().Replace(",", ".")+",";
        data_string += transform.rotation.x.ToString().Replace(",", ".")+",";
        data_string += MoveDrone.SumThrust.ToString().Replace(",", ".")+",";
        data_string += 0.ToString().Replace(",", ".")+",";
        port.Write(data_string);
        Debug.Log(data_string);
    }
}
