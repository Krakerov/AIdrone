using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rot_Drone : MonoBehaviour
{
    private Rigidbody rbGO;
    public Transform Target;
    public float main_thrust_x = 2;
    public float P_x = 2f;
    public float I_x = 0.1f;
    public float i_error_x = 0f;
    public float D_x = 1f;
    float preErr_x = 0;
    public float SumPid_x;
    public float set_x;


    public float i_error_z = 0f;
    float preErr_z = 0;
    public float SumPid_z;
    public float set_z;
    // Start is called before the first frame update
    void Start()
    {
        rbGO = gameObject.GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    void FixedUpdate() {
        set_x = Target.position.x;
        i_error_x += (set_x - transform.position.x)*Time.deltaTime;
        SumPid_x = (set_x - transform.position.x)*P_x + i_error_x*I_x +  (set_x - transform.position.x - preErr_x)/Time.deltaTime*D_x;
        preErr_x = set_x - transform.position.x;
        //rbGO.AddForce(transform.right * SumPid_x*main_thrust_x);
        

        set_z = Target.position.z;
        i_error_z += (set_z - transform.position.z)*Time.deltaTime;
        SumPid_z = (set_z - transform.position.z)*P_x + i_error_z*I_x +  (set_z - transform.position.z - preErr_z)/Time.deltaTime*D_x;
        preErr_z = set_z - transform.position.z;
        //rbGO.AddForce(transform.right * SumPid_x*main_thrust_x);

        rbGO.rotation = Quaternion.Euler(SumPid_z*main_thrust_x, 0, SumPid_x*main_thrust_x*-1);

    }


}
