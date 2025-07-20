import sqlite3
import pandas as pd
import streamlit as st



# Title of the Streamlit app
st.title("🎓 Placement Eligibility Checker")

# SQLite connection
conn = sqlite3.connect("placement_eligibility.db")

# QUERY List
query_type = st.selectbox(
    "Select",
    ["1.Top 10 Students ready for placement",
     "2.Only Male Students who got placed",
     "3.Only Female Students who ready for Placements",
     "4.Students with more than 100 problems solved and interpersonal skills score above 70",
     "5.Students with more than 75 score in latest project",
     "6.Students from batch 'A' who are ready for placement",
     "7.Students from batch 'C' who are placed",
     "8.Students whose language is java and Leadership skills more than 85",
     "9.Students who Completed Three internships and mock interview score above 85",
     "10.Students who has more than 10L package",
     "11.Students who has completed 5 mini projects",
     "12.Students who Completed three internships and ready for placement",
     "13.Company Name's of the Placed Students",
     "14.Student Who got placed age more dhan 25",
     "15.Placement ID of not Ready students",
     "16.Teamwork and Leadeship skills more dhan 80",
     "17.Students Cleared Four interview rounds",
     "18.Students have more than 75 score on both Communication,Presentation and Critical thinking",
     "19.Get me the Student Details",
     "20.City,Phone_number and Email of Placed Students",
     "21.Average soft skill per batch",
     "22.To chek Placement Status Count"
    ]
    
)

df_results = pd.DataFrame()  #Initialisation of df_results


if query_type =="1.Top 10 Students ready for placement":
   base_query = """
   SELECT S.student_id, S.name,
          ((SS.communication + SS.teamwork + SS.presentation + SS.leadership + SS.critical_thinking + SS.interpersonal_skills)/6.0) AS avg_soft_skills
   FROM Students S
   JOIN SoftSkills SS ON S.student_id = SS.student_id
   WHERE SS.communication >= 0 -- You can adjust this filter as needed
   ORDER BY avg_soft_skills DESC
   LIMIT 10;
   """
   df_results = pd.read_sql_query(base_query, conn)

elif query_type =="2.Only Male Students who got placed":
    base_query = """
    SELECT S.name, S.student_id, S.gender, PL.placement_id
    FROM Students S
    JOIN Placements PL ON S.student_id = PL.student_id
    WHERE S.gender = 'Male' AND PL.placement_status = 'Placed'
    """
    df_results = pd.read_sql_query(base_query, conn)

elif query_type =="3.Only Female Students who ready for Placements":
    base_query = """
    SELECT S.name, S.student_id,S.gender,PL.placement_status, PL.placement_id, PL.mock_interview_score,PL.internships_completed
    FROM Students S
    JOIN Placements PL ON S.student_id = PL.student_id
    WHERE S.gender='Female' AND PL.placement_status= 'Ready'
    """

    df_results = pd.read_sql_query(base_query,conn)

elif query_type =="4.Students with more than 100 problems solved and interpersonal skills score above 70":
    base_query = """
    SELECT S.name, S.student_id,P.programming_id, P.problems_solved, SS.interpersonal_skills
    FROM Students S
    JOIN Programming P ON S.student_id=P.student_id
    JOIN SoftSkills SS ON S.student_id=SS.student_id
    WHERE P.problems_solved > 100 AND SS.interpersonal_skills > 70
    """
    df_results =pd.read_sql_query(base_query,conn)

elif query_type =="5.Students with more than 75 score in latest project":
    base_query = """
    SELECT S.name, P.latest_project_score
    FROM Students S
    JOIN Programming P ON S.student_id = P.student_id
    WHERE P.latest_project_score>75
    """
    df_results = pd.read_sql_query(base_query,conn)

elif query_type =="6.Students from batch 'A' who are ready for placement":
    base_query = """
    SELECT S.student_id, S.name ,S.course_batch, PL.placement_status
    FROM Students S
    JOIN Placements PL ON S.student_id = PL.student_id
    WHERE S.course_batch= 'A' AND PL.placement_status= 'Ready'
    """
    df_results=pd.read_sql_query(base_query,conn)

elif query_type =="7.Students from batch 'C' who are placed":
    base_query = """
    SELECT S.student_id, S.name, S.course_batch, PL.placement_status
    FROM Students S
    JOIN Placements PL ON S.student_id= PL.student_id
    WHERE S.course_batch= 'C' AND PL.placement_status= 'Placed'
    """

    df_results=pd.read_sql_query(base_query,conn)

elif query_type =="8.Students whose language is java and Leadership skills more than 85":
    base_query = """
    SELECT S.name, P.language,SS.leadership
    FROM Students S
    JOIN Programming P ON S.student_id=P.student_id
    JOIN SoftSkills SS ON S.student_id=SS.student_id
    WHERE P.language='Java' AND SS.leadership > 85
    """
    df_results=pd.read_sql_query(base_query,conn)

elif query_type =="9.Students who Completed Three internships and mock interview score above 85":
    base_query = """
    SELECT S.name,PL.internships_completed,PL.mock_interview_score
    FROM Students S
    JOIN Placements PL ON S.student_id= PL.student_id
    Where PL.internships_completed = 3 and PL.mock_interview_score > 85
    """
    df_results=pd.read_sql_query(base_query,conn)

elif query_type =="10.Students who has more than 10L package":
    base_query = """
    SELECT S.name,PL.placement_package
    FROM Students S
    JOIN Placements PL ON S.student_id=PL.student_id
    Where PL.placement_package > 1000000
    """
    df_results=pd.read_sql_query(base_query,conn)

elif query_type =="11.Students who has completed 5 mini projects":
    base_query = """
    SELECT S.name,P.mini_projects
    FROM Students S
    JOIN Programming P ON S.student_id=P.student_id
    Where P.mini_projects = 5
    """
    df_results=pd.read_sql_query(base_query,conn)

elif query_type =="12.Students who Completed three internships and ready for placement":
    base_query = """
    SELECT S.name,PL.internships_completed,PL.placement_status
    FROM Students S
    JOIN Placements PL ON S.student_id=PL.student_id
    Where PL.internships_completed > 2 AND PL.placement_status='Ready'
    """
    df_results=pd.read_sql_query(base_query,conn)

elif query_type =="13.Company Name's of the Placed Students":
    base_query = """
    SELECT S.name,PL.placement_status, PL.company_name,PL.placement_date
    FROM Students S
    JOIN Placements PL ON S.student_id=PL.student_id
    Where PL.placement_status = 'Placed'
    """
    df_results=pd.read_sql_query(base_query,conn)


elif query_type =="14.Student Who got placed age more dhan 25":
    base_query = """
    SELECT S.name,S.age, PL.placement_status
    FROM Students S
    JOIN Placements PL ON S.student_id=PL.student_id
    Where S.age > 25 and PL.placement_status ='Placed'
    """
    df_results=pd.read_sql_query(base_query,conn)

elif query_type =="15.Placement ID of not Ready students":
    base_query = """
    SELECT  PL.placement_status, PL.placement_id, S.name
    FROM Students S
    JOIN Placements PL ON S.student_id=PL.student_id
    Where PL.placement_status ='Not Ready'
    """
    df_results=pd.read_sql_query(base_query,conn)

elif query_type =="16.Teamwork and Leadeship skills more dhan 80":
    base_query = """
    SELECT  SS.teamwork, SS.leadership, S.name
    FROM Students S
    JOIN SoftSkills SS ON S.student_id=SS.student_id
    Where SS.teamwork > 80 AND SS.leadership >80
    """
    df_results=pd.read_sql_query(base_query,conn)

elif query_type =="17.Students Cleared Four interview rounds":
    base_query = """
    SELECT  PL.interview_rounds_cleared, S.name
    FROM Students S
    JOIN Placements PL ON S.student_id= PL.student_id
    Where PL.interview_rounds_cleared >= 4
    """
    df_results=pd.read_sql_query(base_query,conn)

elif query_type =="18.Students have more than 75 score on both Communication,Presentation and Critical thinking":
    base_query = """
    SELECT S.name, SS.communication, SS.presentation, SS.critical_thinking  
    FROM Students S
    JOIN SoftSkills SS ON S.student_id=SS.student_id
    WHERE SS.communication > 75 AND SS.presentation > 75 AND SS.critical_thinking > 75
    """
    df_results=pd.read_sql_query(base_query,conn)

elif query_type == "19.Get me the Student Details":
    student_name = st.sidebar.text_input("🔎Enter Student Name")
    
    if student_name and student_name.strip():
        base_query = """
        SELECT S.student_id, S.name, S.age, S.gender, S.email, S.phone, S.enrollment_year, S.course_batch, S.city, S.graduation_year,
               P.programming_id, P.language, P.problems_solved, P.assessments_completed, P.mini_projects, P.certifications_earned, P.latest_project_score,
               SS.soft_skill_id, SS.communication, SS.teamwork, SS.presentation, SS.leadership, SS.critical_thinking, SS.interpersonal_skills,
               PL.placement_id, PL.mock_interview_score, PL.internships_completed, PL.placement_status, PL.company_name, PL.placement_package, PL.interview_rounds_cleared, PL.placement_date
        FROM Students S
        JOIN Programming P ON S.student_id = P.student_id
        JOIN SoftSkills SS ON S.student_id = SS.student_id
        JOIN Placements PL ON S.student_id = PL.student_id
        WHERE S.name = ?
        """
        params = (student_name.strip(),) #To remove leading/trailing spaces
        df_results = pd.read_sql_query(base_query, conn, params=params)
        if df_results.empty:
            st.warning("No student found with the given name.")
    

elif query_type =="20.City,Phone_number and Email of Placed Students":
    base_query = """
    SELECT S.name, S.city, S.phone, S.email, PL.placement_status    
    FROM Students S
    JOIN Placements PL ON S.student_id=PL.student_id
    WHERE PL.placement_status = 'Placed'
    """
    df_results=pd.read_sql_query(base_query,conn)   

elif query_type =="21.Average soft skill per batch":
    base_query = """
    SELECT S.course_batch,
    AVG(SS.communication) AS avg_communication,
    AVG(SS.teamwork) AS avg_teamwork,
    AVG(SS.presentation) AS avg_presentation
    FROM Students S
    JOIN SoftSkills SS ON S.student_id = SS.student_id
    GROUP BY S.course_batch
    """
    df_results = pd.read_sql_query(base_query, conn)

elif query_type =="22.To chek Placement Status Count":
    base_query = """
    SELECT PL.placement_status, COUNT(*) AS count
    FROM Placements PL
    GROUP BY PL.placement_status
    """
    df_results = pd.read_sql_query(base_query, conn)




if df_results is not None and not df_results.empty:#To check if df_results is not empty

    df_results = df_results.fillna("").astype(str)
    
    st.subheader("✅ Query Results")#Header for results
    st.dataframe(df_results)

# Close the connection after query

conn.close()