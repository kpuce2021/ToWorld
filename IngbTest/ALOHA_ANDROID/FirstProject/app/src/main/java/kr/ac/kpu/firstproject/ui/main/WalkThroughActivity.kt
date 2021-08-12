package kr.ac.kpu.firstproject.ui.main

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.viewpager.widget.ViewPager
import kr.ac.kpu.firstproject.R
import me.relex.circleindicator.CircleIndicator

class WalkThroughActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_walk_through)

        /* 어댑터와 뷰페이지 연결 : 스와이프로 넘기는 것 */

        val sectionsPagerAdapter = SectionsPagerAdapter(this, supportFragmentManager) // Adapter 객체 생성
        val viewPager: ViewPager = findViewById(R.id.view_pager) // view가 보여질 부분에 viewPagerAdapter로 지정
        viewPager.adapter = sectionsPagerAdapter

        val indicator: CircleIndicator = findViewById(R.id.indicator)
        indicator.setViewPager(viewPager) // 인디케이터 똥그라미 작은거 이게 viewPager를 참조해서 왔다리 갔다리

    }
}